from types import SimpleNamespace

def get_unique_elements(list1, list2):
    unique1 = [item for item in list1 if item not in list2]
    unique2 = [item for item in list2 if item not in list1]
    return unique1, unique2

def diff_dfgs(dfg1, dfg2):

    nodes1 = dfg1.nodes
    nodes2 = dfg2.nodes
    unique_nodes1, unique_nodes2 = get_unique_elements(nodes1, nodes2)
    
    edges1 = dfg1.edges.keys()
    edges2 = dfg2.edges.keys()
    unique_edges1, unique_edges2 = get_unique_elements(edges1, edges2)
    

    im1 = dfg1.im.keys()
    im2 = dfg2.im.keys()
    unique_im1, unique_im2 = get_unique_elements(im1, im2)

            
    fm1 = dfg1.fm.keys()
    fm2 = dfg2.fm.keys()
    unique_fm1, unique_fm2 = get_unique_elements(fm1, fm2)   
    
    
  
    diff = {
        "unique_nodes1": unique_nodes1,
        "unique_nodes2": unique_nodes2,
        "unique_edges1": unique_edges1,
        "unique_edges2": unique_edges2,
        "unique_im1": unique_im1,
        "unique_im2": unique_im2,
        "unique_fm1": unique_fm1,
        "unique_fm2": unique_fm2,
    }
    
    return SimpleNamespace(**diff)
    
    
    
    
