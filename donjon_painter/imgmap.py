from pathlib import Path
from PIL import Image
from random import choice


# Actually create the map in question
def generateMap(args, mapBlocks, resFile):
    if mapBlocks is not False and resFile != []:
        # Scale theme tiles to desired size
        for supKey, category in mapBlocks.items():
            for key, img in category.items():
                mapBlocks[supKey][key] = mapBlocks[supKey][key].resize(
                    (args.pixels, args.pixels),
                    resample=Image.LANCZOS)

        # Convert all tiles to RGBA mode
        for supKey, category in mapBlocks.items():
            for key, img in category.items():
                if mapBlocks[supKey][key].mode != 'RGBA':
                    mapBlocks[supKey][key] = mapBlocks[supKey][key].convert(
                        'RGBA'
                    )

        # Get width & height of image
        # width = len(resFile[0]) * args.pixels
        # height = len(resFile) * args.pixels
        # Get width & height of image using tiles with an alpha border
        width = (len(resFile[0])+2) * args.pixels//3
        height = (len(resFile)+2) * args.pixels//3

        # Paste images onto blank canvas
        tmpImage = Image.new('RGBA', (width, height))
        if mapBlocks is not False:
            for row, tileMap in enumerate(resFile):
                # yPos = row * args.pixels
                yPos = row * (args.pixels-3) // 3
                # Loop through tile resources in single tile
                for col, tileArray in enumerate(tileMap):
                    # xPos = col * args.pixels
                    xPos = col * (args.pixels-3) // 3
                    # Merge resources if there's more than one
                    if len(tileArray) > 1:
                        tileImage = Image.new(
                            'RGBA', (args.pixels, args.pixels)
                        )
                        for pos, imgCur in enumerate(tileArray):
                            if pos == (len(tileArray) - 1):
                                break
                            imgNext = tileArray[pos+1]
                            bg = mapBlocks[imgCur[0]][imgCur[1]]
                            fg = mapBlocks[imgNext[0]][imgNext[1]]
                            tileImage = Image.alpha_composite(
                                tileImage, bg)
                            tileImage = Image.alpha_composite(
                                tileImage, fg)
                        # tmpImage.paste(im=tileImage, box=(xPos, yPos))
                            tmpImage.alpha_composite(
                                im=tileImage,
                                dest=(xPos, yPos)
                            )
                    else:
                        # Floor tile randomising
                        tileCat = tileArray[0][0]
                        tileNam = tileArray[0][1]
                        if args.randomise and tileNam == 'floor':
                            floorImg = mapBlocks[tileCat][tileNam]
                            floorImg = choice([
                                floorImg,
                                floorImg.transpose(Image.ROTATE_90),
                                floorImg.transpose(Image.ROTATE_180),
                                floorImg.transpose(Image.ROTATE_270)
                            ])
                            # tmpImage.paste(im=floorImg, box=(xPos, yPos))
                            tmpImage.alpha_composite(
                                im=floorImg,
                                dest=(xPos, yPos)
                            )
                        else:
                            # tmpImage.paste(
                            #     im=mapBlocks[tileCat][tileNam],
                            #     box=(xPos, yPos)
                            # )
                            tmpImage.alpha_composite(
                                im=mapBlocks[tileCat][tileNam],
                                dest=(xPos, yPos)
                            )
        return tmpImage
    else:
        return False


# Save map to a specific directory
def writeMap(args, tmpMap):

    if tmpMap is not False:
        defName = 'Map.png'
        defLocs = Path.home()
        saveLoc = Path(args.output).expanduser()

        fileTypes = ['.png', '.jpg', '.jpeg']

        if saveLoc.is_dir():
            saveLoc = Path(saveLoc, defName)
            tmpMap.save(saveLoc)
        elif saveLoc.parent.is_dir():
            if saveLoc.suffix in fileTypes:
                tmpMap.save(saveLoc)
            else:
                saveLoc = str(saveLoc) + '.png'
                tmpMap.save(saveLoc)
        else:
            saveLoc = str(Path(defLocs, defName))
            tmpMap.save(saveLoc)
    else:
        return False
