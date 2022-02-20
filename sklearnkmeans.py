from sklearn.cluster import KMeans  
import matplotlib.pyplot as plt
import numpy as np
import PIL
from data_preprocessing import *


img=PIL.Image.open('img10.jpg').convert('RGB')
# img=img.resize((100,100)) # width , height
img=img.resize((200,200)) # width , height
# img=img.rotate(90)
# img.show()
x=np.array(img)
x=x.reshape(-1,3)

# scaler=feature_scaling(x)  # maybe this is necessary
# x=scaler.transform(x)
x=x/255

model=KMeans(n_clusters=6, init='k-means++', random_state= 42)
# model.random_initializations(x,iter=100,num_of_models=10)
model.fit(x)
# colors=model.mu # gets the average colors



idx=model.predict(x)
# print(idx)
colors=model.cluster_centers_
# colors=scaler.transform_to_normal(colors).astype('uint8')
colors=(colors*255).astype('uint8')
model.K=model.n_clusters
# print(colors)

# for k in range(model.K):   # gets the a sample of the cluster from the image
#     all_colors=x[(k==model.x_cluster_idx(x)),:]
#     idx=np.random.choice(all_colors.shape[0],1)
#     color=all_colors[idx]
#     # print(color.shape)
#     if k==0:
#         colors=color
#     colors=np.r_[colors,color]
# print(colors.shape)

fig=plt.figure()
plt.title("sk kmeans")
plt.axis('off')
for i in range(model.K):
    fig.add_subplot(1,model.K+1,i+1)
    color=np.tile(colors[i,:],4*4).reshape(4,4,3)
    plt.title(f'color {i+1}')
    plt.axis('off')
    plt.imshow(color)

fig.add_subplot(1,model.K+1,i+1+1)
plt.title('image')
plt.axis('off')
plt.imshow(np.array(img))
plt.savefig("sk kmeans.png")
plt.show()