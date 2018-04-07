import matplotlib.pyplot as plt


'''
points -> 2D np array
clearFlag -> boolean to clear the prev points or not
'''

def visualizeScan(points, clearFlag):
    fig = plt.figure(1);
    ax = fig.add_subplot(111); 
    if (clearFlag):
        ax.clear();
    x = points[:,0];
    y = points[:,1]; 
    ax.scatter(x,y);
    plt.axis('equal');
    fig.canvas.draw(); 
    plt.show(block=False);

