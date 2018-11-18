import pandas as pd
import geoviews as gv
import holoviews as hv
import holoviews.plotting.bokeh
from bokeh.layouts import widgetbox,layout
from bokeh.models import Select,RangeSlider,LinearColorMapper
from bokeh.palettes import viridis
from bokeh.plotting import curdoc
import jusipy
from holoviews.operation import decimate
from sklearn import preprocessing
import numpy as np

renderer = hv.renderer('bokeh').instance(mode='server')
gv.extension('bokeh')

loc_feats = pd.read_pickle('data/grid_1000_imputed_features.pkl')
locs = pd.read_pickle('data/grid_1000.pkl')
loc_feats['Longitude'] = locs.long
loc_feats['Latitude'] = locs.lat
temp = pd.read_pickle('data/grid_1000_risk_scores.pkl')
loc_feats['Risk Score'] = temp.rf.values
TOOLS = ['hover','crosshair','zoom_in','zoom_out','tap','box_select']
features=list(loc_feats.columns)[:-3]
cols = loc_feats.columns
loc_norm = loc_feats[features]
loc_feats[features] = pd.DataFrame(preprocessing.normalize(np.array(loc_norm)),columns=features)

cur_var = 'Risk Score'
temp_feats = loc_feats
feats = gv.Dataset(temp_feats, kdims=['Longitude','Latitude',cur_var])
points = feats.to(gv.Points, ['Longitude', 'Latitude'], [cur_var])
tiles = gv.tile_sources.CartoEco
cur_size = 5

max_cur_feature = temp_feats['Risk Score'].max()
min_cur_feature = temp_feats['Risk Score'].min()
world_map = decimate(gv.Points(points),max_samples=20000).options('Points',size=cur_size,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,global_extent=True,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.4)

def update_map(attr, old, new):
    global selection,vizual,gvplot,hvplot,heatmap,feats,points,world_map,range_slider,controls3,max_cur_feature,min_cur_feature,temp_feats
    max_cur_feature = temp_feats[choice.value].max()
    min_cur_feature = temp_feats[choice.value].min()
    range_slider = RangeSlider(start=min_cur_feature, end=max_cur_feature, value=(min_cur_feature,max_cur_feature), step=(max_cur_feature - min_cur_feature)/20, title="Feature_range")
    range_slider.on_change('value', update_map_val)
    controls3 = widgetbox([range_slider], width=250)
    new_loc_feats = temp_feats.loc[(temp_feats[choice.value] < range_slider.value[1]) & (temp_feats[choice.value] > range_slider.value[0])]
    feats = gv.Dataset(new_loc_feats, kdims=['Longitude','Latitude',new])   
    points = feats.to(gv.Points, ['Longitude', 'Latitude'], [new])
    if len(new_loc_feats) <= 20000:
        world_map = gv.Overlay(tiles*points).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,global_extent=True,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
    else:
        world_map = decimate(gv.Points(points),max_samples=20000).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,global_extent=True,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
    selection = hv.streams.Selection1D(source=world_map)
    heatmap = hv.DynamicMap(selected_points,streams=[selection])
    zoom =  hv.DynamicMap(test_bounds, streams=[box])
    hvplot = renderer.get_plot(heatmap,curdoc())
    gvplot = renderer.get_plot(world_map,curdoc())
    bvplot = renderer.get_plot(zoom,curdoc())
    vizual.children[1].children = [gvplot.state,hvplot.state,bvplot.state]


def update_heatmap(attr,old,new):
    global data,ids
    data = []
    ids.reverse()
    if len(ids) == 1:
        selection.event(index=[])
    else:
        selection.event(index=ids)


def update_map_val(attr,old,new):
    global selection,vizual,gvplot,hvplot,heatmap,feats,points,world_map,temp_feats
    max_cur_feature = loc_feats[choice.value].max()
    min_cur_feature = loc_feats[choice.value].min()
    new_loc_feats = temp_feats.loc[(temp_feats[choice.value] <= new[1]) & (temp_feats[choice.value] >= new[0])]
    feats = gv.Dataset(new_loc_feats, kdims=['Longitude','Latitude',choice.value])
    points = feats.to(gv.Points, ['Longitude', 'Latitude'], [choice.value])
    if len(new_loc_feats) <= 20000:
        world_map = gv.Points(points).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
    else:
        world_map = decimate(gv.Points(points),max_samples=20000).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
    selection = hv.streams.Selection1D(source=world_map)
    heatmap = hv.DynamicMap(selected_points,streams=[selection])
    box = hv.streams.BoundsXY(source=world_map)
    zoom =  hv.DynamicMap(test_bounds, streams=[box])
    hvplot = renderer.get_plot(heatmap,curdoc())
    gvplot = renderer.get_plot(world_map,curdoc())
    bvplot = renderer.get_plot(zoom,curdoc())
    vizual.children[1].children = [gvplot.state,hvplot.state,bvplot.state]

ids = list(temp_feats.index)
data = []
selection = hv.streams.Selection1D(source=world_map)
choice = Select(title='Displayed Variable', value='Risk Score', options=['Risk Score']+features)
choice.on_change('value', update_map)
controls = widgetbox([choice], width=300)

weights = pd.read_pickle('data/model_weights.pkl')
models = ['Random Forest', 'Logistic Regression']
weights.columns =['Feature','Logistic Regression', 'Random Forest']
weights = weights.sort_index()
models_feats_imp = {}
for i in models:
    models_feats_imp[i] = weights[i].iloc[:len(features)] 
    
choice2 = Select(title='Prediction Model', value='Random Forest', options=models)
choice2.on_change('value', update_heatmap)
controls2 = widgetbox([choice2], width=250)

max_cur_feature = temp_feats[choice.value].max()
min_cur_feature = temp_feats[choice.value].min()
range_slider = RangeSlider(start=min_cur_feature, end=max_cur_feature, value=(min_cur_feature,max_cur_feature), step=(max_cur_feature - min_cur_feature)/20, title="Feature_range")
range_slider.on_change('value', update_map_val)
controls3 = widgetbox([range_slider], width=250)

def selected_points(index):
    global data,ids
    if len(ids) == 1 and index == []:
        index = ids
    if index and len(index) <= 1000:
        for i in index:
            for j in range(len(features)):
                data.append((features[j],str(i),temp_feats[features[j]].iloc[i] * models_feats_imp[choice2.value][j]))
        b=temp_feats.iloc[index][features].mean()
        c=temp_feats.iloc[0:len(loc_feats)][features].mean()
        for j in range (len(features)):
            data.append((features[j],'Mean_value',b[features[j]]* models_feats_imp[choice2.value][j]))
        if ids == []:
            ids = index
        elif ids != index:
            ids += index
    else:
        data = []
        ids = []
    return hv.HeatMap(data,kdims=['Points','Features'],vdims=['Values']).options(colorbar=True,width=950,height=800,tools=TOOLS,xrotation=45).sort()

def test_bounds(bounds):
    global selection,vizual,gvplot,hvplot,heatmap,feats,points,world_map,range_slider,controls3,max_cur_feature,min_cur_feature,temp_feats
    if bounds != None:
        min_long = min(bounds[0],bounds[2])
        max_long = max(bounds[0],bounds[2])
        min_lat = min(bounds[1],bounds[3])
        max_lat = max(bounds[1],bounds[3])
        downscale_feats = loc_feats.loc[(loc_feats['Longitude'] >= min_long) & (loc_feats['Longitude'] <= max_long) & (loc_feats['Latitude'] >= min_lat) & (loc_feats['Latitude'] <= max_lat)]
        temp_feats = downscale_feats
        max_cur_feature = temp_feats[choice.value].max()
        min_cur_feature = temp_feats[choice.value].min()
        range_slider = RangeSlider(start=min_cur_feature, end=max_cur_feature, value=(min_cur_feature,max_cur_feature), step=(max_cur_feature - min_cur_feature)/20, title="Feature_range")
        range_slider.on_change('value', update_map_val)
        controls3 = widgetbox([range_slider], width=250)
        new_loc_feats = temp_feats.loc[(temp_feats[choice.value] <= range_slider.value[1]) & (temp_feats[choice.value] >= range_slider.value[0])]
        feats = gv.Dataset(new_loc_feats, kdims=['Longitude','Latitude',choice.value])
        points = feats.to(gv.Points, ['Longitude', 'Latitude'], [choice.value])
        if len(new_loc_feats <= 20000):
            world_map = gv.Points(points).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
        else:
           world_map = decimate(gv.Points(points),max_samples=20000).options('Points',size=5,cmap='viridis',colorbar=True,tools=TOOLS,color_index=2,width=900,height=800,colorbar_opts={'scale_alpha':0.5},fill_alpha=0.5,line_alpha=0.5)
        selection = hv.streams.Selection1D(source=world_map)
        heatmap = hv.DynamicMap(selected_points,streams=[selection])
        box = hv.streams.BoundsXY(source=world_map)
        zoom =  hv.DynamicMap(test_bounds, streams=[box])
        hvplot = renderer.get_plot(heatmap,curdoc())
        gvplot = renderer.get_plot(world_map,curdoc())
        bvplot = renderer.get_plot(zoom,curdoc())
        vizual.children[1].children = [gvplot.state,hvplot.state,bvplot.state]
        vizual.children[0].children[2] = controls3
    else:
        bounds = (0,0,0,0)
    return hv.Bounds(bounds).options(show_grid=False,height=0,width=0,xaxis=None,yaxis=None,default_tools=[],show_frame=False,toolbar=None)
    
box = hv.streams.BoundsXY(source=world_map)
zoom = hv.DynamicMap(test_bounds, streams=[box])
ids = []
heatmap = hv.DynamicMap(selected_points,streams=[selection])
hvplot = renderer.get_plot(heatmap,curdoc())
gvplot = renderer.get_plot(world_map,curdoc())
bvplot = renderer.get_plot(zoom,curdoc())
vizual = layout([controls,widgetbox([],width=400),controls3,widgetbox([],width=650),controls2],[gvplot.state,hvplot.state,bvplot.state],sizing_mode='fixed')
curdoc().add_root(vizual)
doc = curdoc()
doc.title = 'Asser Viz Prototype'
