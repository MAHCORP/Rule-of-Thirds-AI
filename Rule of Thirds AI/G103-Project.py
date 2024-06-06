import cv2
import os
import matplotlib.pyplot as plt

#overlay function creates the rule of third grid based on the parameters given
def overlay(image):
    height, width = image.shape[:2] 
    qwidth = width // 3
    qheight = height // 3

#verticle lines
    cv2.line(image, (qwidth, 0), (qwidth, height), (255, 0, 0), 2)
    cv2.line(image, (2 * qwidth, 0), (2 * qwidth, height), (255, 0, 0), 2)

#horizontal lines
    cv2.line(image, (0, qheight), (width, qheight), (255, 0, 0), 2)
    cv2.line(image, (0, 2 * qheight), (width, 2 * qheight), (255, 0, 0), 2)

    return image

#loads image into func and applies rule of thirds and overlay with an added fail case
def applyRot(originalPath):
    img = cv2.imread(originalPath)
    if img is None:
        print("There was an error in loading the file. Please try again ")
        return
    
    height, width = img.shape[:2]
    qwidth = width // 3
    qheight = height // 3

#determine main subject points close to center 
    hWidth = 2 * qwidth
    hHeight = 2 * qheight

# find nearest divisdion from center 
    xCord = min(qwidth, qwidth, key=lambda x: abs(x - width // 2))
    yCord = min(qheight, hHeight, key=lambda x: abs(x - height // 2))

#calculate modified image coodinates
    n_lSide = max(xCord - width // 2, 0)
    n_tSide = max(yCord - height // 2, 0)
    n_rSide = min(xCord + width // 2, width)
    n_bSide = min(yCord + height // 2, height)

#overlay image with the rule of third
    newImage = img[n_tSide:n_bSide, n_lSide:n_rSide]
    rotOverlay = overlay(newImage)

    path = os.path.splitext(originalPath)[0] + 'desiredImage.jpg'
    cv2.imwrite(path, rotOverlay)

    return path, newImage

#displayes dimensions and ratios of both images 
def dimAndRat(nPath):
    unchangedim = cv2.imread(nPath)

    if unchangedim is None:  
        print("There was an error in loading the file. Please try again")
        return

    newPath, newImage = applyRot(nPath)

    regHeight, oneWidth = unchangedim.shape[:2]
    newHeight, twoWidth = newImage.shape[:2]

    regRatio = oneWidth / regHeight
    newRatio = twoWidth / newHeight

    # Display information on a single plot
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
     
     # Bar graphs for dimensions and aspect ratios
    labels = ['Original', 'Modified']
    dimensions = [oneWidth * regHeight, twoWidth * newHeight]
    ratios = [regRatio, newRatio]

    ax[1, 0].bar(labels, dimensions, color=['blue', 'green'])
    ax[1, 0].set_title('Image Dimensions (widthxheight)')
    ax[1, 0].set_ylabel('Dimension (pixels)')

    ax[1, 1].bar(labels, ratios, color=['blue', 'green'])
    ax[1, 1].set_title('Ratios (width/height)')
    ax[1, 1].set_ylabel('Ratio')
    # Show images
    ax[0, 0].imshow(cv2.cvtColor(unchangedim, cv2.COLOR_BGR2RGB))
    ax[0, 0].set_title('Original Image')
    ax[0, 0].axis('off')

    ax[0, 1].imshow(cv2.cvtColor(newImage, cv2.COLOR_BGR2RGB))
    ax[0, 1].set_title('New Image')
    ax[0, 1].axis('off')

  

    plt.tight_layout()
    plt.show()

# Example usage
nPath = "please copy image path here "
dimAndRat(nPath)