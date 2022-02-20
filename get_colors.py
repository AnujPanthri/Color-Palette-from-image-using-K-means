from k_means import k_means
import matplotlib.pyplot as plt
import numpy as np
import PIL
from data_preprocessing import *


img=PIL.Image.open('img4.jpg').convert('RGB')   # change image's name to which ever image you want to run k-means on
# img=img.resize((100,100)) # width , height
img=img.resize((200,200)) # width , height
# img=img.rotate(90)
# img.show()
x=np.array(img)
x=x.reshape(-1,3)

# scaler=feature_scaling(x)  # maybe this is necessary
# x=scaler.transform(x)
x=x/255

model=k_means(6)    # set number of colors you wanna generate
model.random_initializations(x,num_of_models=3)    # we use the best of 3 random initializations to make sure we dont get stuck local optima
# model.elbow_method(x,K=6)
# hist=model.train(x,showat=1)
hist=model.train(x,show=False)
# model.loss_graph(hist)

_,idx=model.x_cluster_idx(x,return_nearest_idx=True)
colors=x[idx,:]
print(colors.shape)

# colors=model.mu # gets the average colors

# colors=scaler.transform_to_normal(colors).astype('uint8')
colors=(colors*255).astype('uint8')
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

out=model.x_cluster_idx(x)
color_support=[np.sum((out==k)*1) for k in range(model.K)]
# print('pred:',out.shape)
# print(out[:5])

most_dominent=np.tile(colors[np.argmax(color_support),:],4*4).reshape(4,4,3)    # 4x4x3 image of the most dominating color from the image
# plt.figure()
# plt.imshow(most_dominent) # to show the most dominent color
# plt.show()

fig=plt.figure()
# fig=plt.figure(figsize=(200,150))
plt.title("my kmeans")
plt.axis('off')
for i in range(model.K):
    mask=(out==i)*1
    h,w,_=np.array(img).shape
    mask_img=(np.array(img)*mask.reshape(h,w,1)).astype('uint8')
    color=np.tile(colors[i,:],4*4).reshape(4,4,3)

    fig.add_subplot(2,model.K+1,i+1)
    if np.argmax(color_support)==i:
        plt.title(f'Dominent color {i+1} ({color_support[i]})')
    else:
        plt.title(f'color {i+1} ({color_support[i]})')
    plt.axis('off')
    plt.imshow(color)

    fig.add_subplot(2,model.K+1,((model.K+1)+i+1))
    plt.title(f'mask {i+1}')
    plt.axis('off')
    plt.imshow(mask_img)

fig.add_subplot(2,model.K+1,i+1+1)
plt.title('image')
plt.axis('off')
plt.imshow(np.array(img))
plt.savefig("my kmeans.png",dpi=300)
plt.show()