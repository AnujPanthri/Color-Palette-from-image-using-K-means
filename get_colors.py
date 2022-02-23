from k_means import k_means
import matplotlib.pyplot as plt
import numpy as np
import PIL


def get_colors(x,K=6,show=False):
    '''
    Input: x:array of image
    return:  colors,color_support
    '''
    img=x.copy()
    x=x.reshape(-1,3)
    x=x/255

    model=k_means(K)    # set number of colors you wanna generate
    model.random_initializations(x,num_of_models=4)    # we use the best of 3 random initializations to make sure we dont get stuck local optima
    hist=model.train(x,show=False)

    _,idx=model.x_cluster_idx(x,return_nearest_idx=True)
    colors=x[idx,:]
    # print(colors.shape)

    # colors=model.mu # gets the average colors

    # colors=scaler.transform_to_normal(colors).astype('uint8')
    colors=(colors*255).astype('uint8')
    

    out=model.x_cluster_idx(x)
    color_support=[np.sum((out==k)*1) for k in range(model.K)]

    # most_dominent=np.tile(colors[np.argmax(color_support),:],4*4).reshape(4,4,3)    # 4x4x3 image of the most dominating color from the image
    if show:
        print(colors)
        # plt.close(5)
        fig=plt.figure()
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
        plt.show()
        # plt.close(5)
    return  colors,color_support

    