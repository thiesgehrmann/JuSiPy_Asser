from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import MeanShift
from sklearn.mixture import GaussianMixture
import umap

import matplotlib.pylab as plt
import numpy as np
import pandas as pd

class Negative(object):
    """
    Identify potentially negative deals from a random selection

    Neg = Negative(slabels, features, positive_col='positive', autorun=True, **kwargs)
        labels: A dataframe of labels
        features: A dataframe of features (columns are features) Must be none missing! Index corresponds to index of labels
        positive_col : String. The name of the column you want to use in the labels dataframe
        autorun: Run the pipeline automatically
        **kwargs: Arguments for each step (see pca, tsne, cluster and negatives for the parameters)

    properties:
        negatives: A numpy array of labels for each point, corresponding to the input dataframes
                   1 means negative, 0 means positive/not negative

    """
    def __init__(self, labels, features, positive_col='positive', autorun=False, **kwargs):
        """
        Inputs:
            labels: a dataframe of labels
            features: A dataframe of features (columns are features) Must be none missing! Index corresponds to index of labels
            positive_col : String. The name of the column you want to use in the labels dataframe
            autorun: Run the pipeline automatically
            **kwargs: Arguments for each step (see pca, tsne, cluster and negatives for the parameters)
        Output:
            A Negative structure.
            The negative labels can be retrieved with the property 'negatives'

        """
        self._labels    = labels
        self._features  = features
        self._positives = self._labels[positive_col].values
        self._znorm     = None
        self._dimred    = None
        self._clusters  = None
        self._negatives = None
        if autorun:
            self.run(**kwargs)
        #fi
    #edef

    def run(self, dimred='tsne', **kwargs):
        """
        Run the negative selection pipeline

        Typical usage:
            run(dimred='tsne', bandwidth=10) # Seems to be an appropriate bandwidth for tsne
            run(dimred='umap', bandwidth=2)  # Seems to be an appropriate bandwidth for umap
        Input:
            dimred: String. Dimensionality reduction to use [pca|tsne|umap]
            **kwargs: Arguments for the different stages in the pipeline, which include
                * method : String. Type of clustering to use (see) self.cluster() for information
                * bandwidth : Float. STD to use for MeanShift clustering
        """
        if self._znorm is None:
            self.znorm(**kwargs)
            self._dimred = None
        #fi
        if (self._dimred is None) or (dimred is not None):
            if dimred is None:
                dimred = 'tsne'
            #fi

            if dimred == 'pca':
                self.pca(**kwargs)
            elif dimred == 'umap':
                self.umap(**kwargs)
            else:
                self.tsne(**kwargs)
            #fi
            self._clusters = None
        #fi

        if self._clusters is None:
            self.cluster(**kwargs)
            self._negatives    = None
            self._neg_clusters = None
        #fi
        if self._negatives is None:
            self.get_negatives(**kwargs)
        #fi
        return self._negatives
    #edef

    @property
    def negatives(self, **kwargs):
        return self._negatives
    #edef

    def znorm(self, do_znorm=True, **kwargs):
        if (self._features is None) or not (do_znorm):
            self._znorm = self._features
            return None
        #fi
        print('\rPerforming z-normalization for all features')
        self._znorm = (self._features - self._features.mean()) / self._features.std()
        return self._znorm

    def pca(self, **kwargs):
        if self._znorm is None:
            return None
        #fi
        print('\rPerforming PCA')
        pca  = PCA(n_components=2)
        pca_features  = pca.fit_transform(self._znorm)
        self._dimred = pca_features
        return self._dimred
    #edef

    def tsne(self, **kwargs):
        if self._znorm is None:
            return None
        #fi
        print('\rPerforming TSNE')
        tsne = TSNE(n_components=2)
        tsne_features = tsne.fit_transform(self._znorm)
        self._dimred = tsne_features
        return self._dimred
    #edef

    def umap(self, **kwargs):
        if self._znorm is None:
            return None
        #fi
        print('\rPerforming UMAP')
        self._dimred = umap.UMAP().fit_transform(self._znorm)
        return self._dimred
    #edef

    def cluster(self, method=None, bandwidth=10, **kwargs):
        """
        Cluster the embedded data
        Input:
            method: Dimensionality reduction [tsne, umap, pca]
            method: ['meanshift', 'gmm', callable object]
            bandwidth: Float. Size of kernel for meanshift
            **kwargs: arguments for the specific clustering method
        Output:
            an array of cluster IDs (of length # of points in dataset)
        """

        data = self._dimred

        method = method.lower() if isinstance(method, str) else method
        print('\rPerforming Clustering')
        self._clusters = None
        if method == 'gmm':
            self._clusters = GaussianMixture().fit_predict(data)
        elif method == 'meanshift':
            self._clusters = MeanShift(bandwidth=bandwidth).fit(data).labels_
        elif hasattr(method, '__call__'):
            self._clusters = method(data)
        else:
            self._clusters = MeanShift(bandwidth=bandwidth).fit(data).labels_
        #fi
        return self._clusters
    #edef

    def get_negatives(self, threshold=0.95, **kwargs):
        if self._clusters is None:
            return None
        #fi
        def select_negative_clusters(cluster_labels, positive_labels, threshold=.95):
            """
            Select negative clusters based on some clustering of the TSNE space
            Inputs:
                cluster_labels:  np.array: labels from the clustering
                positive_labels: np.array: labels with true positives (0 is unknown/negative, 1 is true positive)
                threshold:       The % of negative samples per cluster that are required to call it negative (default 0.95)
                                 (i.e. 0.05 positive)
            Outputs:
                a list of cluster label IDs that constitute negative clusters
            """
            clusters = list(range(max(cluster_labels)+1))
            neg_clusters = []
            for clust in clusters:
                clust_positive = positive_labels[np.where(cluster_labels == clust)]
                if (sum(clust_positive) / float(len(clust_positive))) < (1-threshold):
                    neg_clusters.append(clust)
                #fi
            #efor
            return neg_clusters
        #edef

        def select_negative_points(cluster_labels, positive_labels, threshold=0.95):
            """
            Select negative clusters based on some clustering of the TSNE space
            Inputs:
                cluster_labels:  np.array: labels from the clustering
                positive_labels: np.array: labels with true positives (0 is unknown/negative, 1 is true positive)
                threshold:       The % of negative samples per cluster that are required to call it negative (default 0.95)
                                 (i.e. 0.05 positive)
            Outputs:
                An array of negative (0) and positive (1) labels
            """
            negative_clusters = select_negative_clusters(cluster_labels, positive_labels, threshold)
            labels = np.array([ 1 ] * len(cluster_labels))
            for nc in negative_clusters:
                labels[np.where(cluster_labels == nc)] = 0
            #efor
            # Correct the true positive points we had which lie in negative clusters
            labels[np.where(positive_labels == 1)] = 1
            return negative_clusters, 1-labels
        #edef
        print('\rSelecting negatives')
        neg_clusters, negatives = select_negative_points(self._clusters, self._positives, threshold=threshold)
        self._neg_clusters = np.array([ 1 if c in neg_clusters else 0 for c in self._clusters ])
        self._negatives = negatives
        return self._negatives
    #edef

    def plot(self):
        """
        Plot the results of the pipeline
        """
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20,30))
        axes = [ ax for row in axes for ax in row ]

        positive_color = '#1b9e77'
        random_color   = '#d95f02'
        negative_color = '#7570b3'

        if ('lat' in self._labels.columns) and ('long' in self._labels.columns):
            lat = self._labels.lat
            long = self._labels.long
            axes[0].set_title('World location')
            axes[0].scatter(long[self._labels.positive==1], lat[self._labels.positive==1],
                            c=positive_color, s=1, zorder=3, label='positive')
            axes[0].scatter(long[self._labels.positive==0], lat[self._labels.positive==0],
                            c=random_color, s=1, zorder=2, label='negative')

            axes[0].set_xlabel('Longitude')
            axes[0].set_ylabel('Latitude')
            axes[0].legend()
        #fi

        if self._dimred is not None:
            axes[1].set_title('Dim.Red. embedding')
            axes[1].scatter(*list(zip(*self._dimred[self._positives==1,:])), c=positive_color, s=1, zorder=2, label='positive')
            axes[1].scatter(*list(zip(*self._dimred[self._positives==0,:])), c=random_color, s=1, zorder=1, label='random')
            axes[1].set_xlabel('Dim.Red. Component 1')
            axes[1].set_ylabel('Dim.Red. Component 2')
            axes[1].legend()
        #fi

        if self._clusters is not None:
            axes[2].set_title('Dim.Red. clustering')
            axes[2].scatter(*list(zip(*self._dimred)), c=self._clusters, s=1)
            axes[2].set_xlabel('Dim.Red. Component 1')
            axes[2].set_ylabel('Dim.Red. Component 2')
            axes[2].legend()
        #fi

        if self._neg_clusters is not None:
            axes[3].set_title('Negative annotation')
            axes[3].scatter(*list(zip(*self._dimred[self._neg_clusters==0,:])), c=positive_color, s=1, zorder=2, label='positive')
            axes[3].scatter(*list(zip(*self._dimred[self._neg_clusters==1,:])), c=negative_color, s=1, zorder=1, label='negative')
            axes[3].set_xlabel('Dim.Red. Component 1')
            axes[3].set_ylabel('Dim.Red. Component 2')
            axes[3].legend()
        #fi

        if self._negatives is not None:
            axes[4].set_title('Negative annotation')
            axes[4].scatter(*list(zip(*self._dimred[self._positives==1,:])), c=positive_color, s=1, zorder=3, label='positive')
            axes[4].scatter(*list(zip(*self._dimred[self._negatives==1,:])), c=negative_color, s=1, zorder=2, label='negative')
            axes[4].scatter(*list(zip(*self._dimred[((self._negatives==0) & (self._positives==0)),:])),
                            c=random_color, s=1, zorder=1, label='random')
            axes[4].set_xlabel('Dim.Red. Component 1')
            axes[4].set_ylabel('Dim.Red. Component 2')
            axes[4].legend()
        #fi

        if (self._negatives is not None) and ('lat' in self._labels.columns) and ('long' in self._labels.columns):
            lat = self._labels.lat
            long = self._labels.long
            axes[5].set_title('World location')
            axes[5].scatter(long[self._positives==1], lat[self._positives==1],
                            c=positive_color, s=1, zorder=3, label='positive')
            axes[5].scatter(long[self._negatives==1], lat[self._negatives==1],
                            c=negative_color, s=1, zorder=2, label='negative')

            axes[5].set_xlabel('Longitude')
            axes[5].set_ylabel('Latitude')
            axes[5].legend()
        #fi

        return fig, axes

    #edef

#eclass


#neg = Negative(all_points, latlong_features, autorun=False)
