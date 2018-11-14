from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import MeanShift
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
    def __init__(self, labels, features, positive_col='positive', autorun=True, **kwargs):
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
        self._pca       = None
        self._tsne      = None
        self._clusters  = None
        self._negatives = None
        if autorun:
            self.run(**kwargs)
        #fi
    #edef

    def run(self, **kwargs):
        """
        Run the negative selection pipeline
        """

        if self._pca is None:
            self.pca(**kwargs)
        #fi
        if self._tsne is None:
            self.tsne(**kwargs)
        #fi
        if self._clusters is None:
            self.cluster(**kwargs)
        #fi
        if self._negatives is None:
            self.negatives(**kwargs)
        #fi
        return self._negatives
    #edef

    @property
    def negatives(self, **kwargs):
        return self._negatives
    #edef

    def pca(self, **kwargs):
        if self._features is None:
            return None
        #fi
        print('\rPerforming PCA')
        pca  = PCA(n_components=2)
        pca_features  = pca.fit_transform(self._features)
        self._pca = pca_features
        return self._pca
    #edef

    def tsne(self, **kwargs):
        if self._features is None:
            return None
        #fi
        print('\rPerforming TSNE')
        tsne = TSNE(n_components=2)
        tsne_features = tsne.fit_transform(self._features)
        self._tsne = tsne_features
        return self._tsne
    #edef

    def cluster(self, bandwidth=10, **kwargs):
        if self._tsne is None:
            return None
        #fi
        print('\rPerforming Clustering')
        self._clusters = MeanShift(bandwidth=bandwidth).fit(self._tsne).labels_
        return self._clusters
    #edef

    def negatives(self, threshold=0.95, **kwargs):
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
            return 1-labels
        #edef
        print('\rSelecting negatives')
        negatives = select_negative_points(self._clusters, self._positives, threshold=threshold)
        self._negatives = negatives
        return negatives
    #edef

    def plot(self):
        """
        Plot the results of the pipeline
        """
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20,20))
        axes = [ ax for row in axes for ax in row ]

        if self._pca is not None:
            axes[0].set_title('PCA embedding')
            axes[0].scatter(*list(zip(*self._pca[self._positives==1,:])), c='g', s=1, zorder=2, label='positive')
            axes[0].scatter(*list(zip(*self._pca[self._positives==0,:])), c='b', s=1, zorder=1, alpha=0.5, label='random')
            axes[0].set_xlabel('PCA Component 1')
            axes[0].set_ylabel('PCA Component 2')
            axes[0].legend()
        #fi

        if self._tsne is not None:
            axes[1].set_title('TSNE embedding')
            axes[1].scatter(*list(zip(*self._tsne[self._positives==1,:])), c='g', s=1, zorder=2, label='positive')
            axes[1].scatter(*list(zip(*self._tsne[self._positives==0,:])), c='b', s=1, zorder=1, alpha=0.5, label='random')
            axes[1].set_xlabel('TSNE Component 1')
            axes[1].set_ylabel('TSNE Component 2')
            axes[1].legend()
        #fi

        if self._clusters is not None:
            axes[2].set_title('TSNE clustering')
            axes[2].scatter(*list(zip(*self._tsne)), c=self._clusters, s=1)
            axes[2].set_xlabel('TSNE Component 1')
            axes[2].set_ylabel('TSNE Component 2')
            axes[2].legend()
        #fi

        if self._negatives is not None:
            axes[3].set_title('Negative annotation')
            axes[3].scatter(*list(zip(*self._tsne[self._positives==1,:])), c='g', s=1, zorder=3, label='positive')
            axes[3].scatter(*list(zip(*self._tsne[self._negatives==1,:])), c='r', s=1, zorder=2, label='negative')
            axes[3].scatter(*list(zip(*self._tsne[((self._negatives==0) & (self._positives==0)),:])),
                            c='b', s=1, zorder=1, alpha=0.5, label='random')
            axes[3].set_xlabel('TSNE Component 1')
            axes[3].set_ylabel('TSNE Component 2')
            axes[3].legend()
        #fi

        return fig, axes
    #edef

#eclass
