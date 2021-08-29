from pathlib import Path
from brownie import (
    network,
    DigiHomie,
    accounts,
    config,
    LinkToken,
    MockV3Aggregator,
    MockOracle,
    VRFCoordinatorMock,
    Contract,
)
from scripts.helpful_scripts import *
from metadata import sample_metadata
from web3 import Web3
from PIL import Image
import numpy as np
import os as os
import json as json
from pathlib import Path
import requests
import numpy as np


def main():
    number = 2
    iteration = 0
    while(iteration <= number):
        # Set homie to current iteration
        digiHomie = DigiHomie[len(DigiHomie)-1]  # Get the most recent
        print("Iteration: " + str(iteration))
        print("Token Counter: " + str(digiHomie.tokenCounter()))
        meta_data = generate_meta_data(iteration)

        # Create image, meta, upload both to ipfs, sets token URI
        # Returns uri (hash) of meta_data on ipfs
        uri = generateHomie(iteration, meta_data)

        # Create homie with
        dev = accounts.add(config['wallets']['from_key'])
        transaction = digiHomie.createHomie(
            uri, {"from": dev})  # no seed needed
        transaction.wait(2)
        iteration = iteration+1  # = to counter?


def generate_meta_data(token_id):
    homie_metadata = sample_metadata.metadata_template
    homie_metadata["name"] = str(token_id)
    homie_metadata["description"] = 'An Eternal Etherium Digital Homie!'
    homie_metadata["image"] = ''
    homie_metadata["background_color"] = '0F7CB3'
    # Will add image and attributes after creation of Homie (image, meta)
    # homie_metadata["attributes"] = [{}]
    return homie_metadata


def get_body(body_number):
    switch = {
        0: 'Thin Light',
        1: 'Thin Mid',
        2: 'Thin Dark',
        3: 'Thick Light',
        4: 'Thick Mid',
        5: 'Thick Dark'
    }
    print(body_number)
    print(switch[body_number])
    return switch[body_number]


def get_eyes(eye_number):
    switch = {
        0: 'Normal',
        1: 'Peep',
        2: 'Squint',
        3: 'Peer',
        4: 'Gold',
    }
    print(eye_number)
    print(switch[eye_number])
    return switch[eye_number]


def get_mouth(mouth_number):
    switch = {
        0: 'Normal',
        1: 'Grin',
        2: 'Smile',
        3: 'Ohh',
        4: 'Lips',
        5: 'Missing Tooth',
        6: 'Gold Tooth'
    }
    print(mouth_number)
    print(switch[mouth_number])
    return switch[mouth_number]

# Optional random generation to include 0 'get_<feature>'


def get_hair(hair_number):
    switch = {
        1: 'Black',
        2: 'Brown',
        3: 'Gray',
        4: 'Pink',
        5: 'Comb-Over',
        6: 'Man-Bun',
        7: 'Corn-Rows',
        8: 'Mullet'
    }
    print(hair_number)
    print(switch[hair_number])
    return switch[hair_number]


def get_facialHair(facialHair_number):
    switch = {
        1: 'Light',
        2: 'Stuble',
        3: 'Handle-Bar Beard',
        4: 'Light Handle-Bar Beard',
        5: 'Grey Beard',
        6: 'Moustache',
        7: 'Handle-Bar'
    }
    print(facialHair_number)
    print(switch[facialHair_number])
    return switch[facialHair_number]


def get_jewelry(jewelry_number):
    switch = {
        1: 'Gold Chain',
        2: 'Gold Chain & Earring',
        3: 'Diamond Chain',
        4: 'Diamond Chain, Earring & Nose Ring',
        5: 'XL Gold Chain & Diamond Earring'
    }
    print(jewelry_number)
    print(switch[jewelry_number])
    return switch[jewelry_number]


def get_smoke(smoke_number):
    switch = {
        1: 'Cigarette',
        2: 'Joint Sativa',
        3: 'Jeferey',
        4: 'Joint Indica'
    }
    print(smoke_number)
    print(switch[smoke_number])
    return switch[smoke_number]


def get_hat(hat_number):
    switch = {
        1: 'Bonzai',
        2: 'Backwards Cap',
        3: 'DuRag',
        4: 'Crown'
    }
    print(hat_number)
    print(switch[hat_number])
    return switch[hat_number]


def get_glasses(glasses_number):
    switch = {
        1: 'Carerra',
        2: 'Miami',
        3: 'Dahmer',
        4: 'Dahmer - Dark',
        5: 'Pink Stunners',
        6: 'Patch'
    }
    print(glasses_number)
    print(switch[glasses_number])
    return switch[glasses_number]


def get_mask(mask_number):
    switch = {
        1: 'Balaklava',
        2: 'Ninja',
        3: 'Doom',
        4: 'Doom 2',
        5: 'Jason'
    }
    print(mask_number)
    print(switch[mask_number])
    return switch[mask_number]


def get_special(special_number):
    switch = {
        1: 'Alien',
        2: 'Death'
    }
    print(special_number)
    print(switch[special_number])
    return switch[special_number]


def generateHomie(token_id, data):

    def generateRandomNumber(lowIn, highIn):
        rng = np.random.default_rng()
        ranNumberArray = rng.integers(low=lowIn, high=highIn, size=1)
        return int(ranNumberArray[0])

    body = generateRandomNumber(1, 6)
    eyes = generateRandomNumber(1, 4)
    mouth = generateRandomNumber(1, 7)
    # OPTIONAL - higher range equals increase randomness, less likely to align with exisiting feature
    hair = generateRandomNumber(0, 8)
    facialHair = generateRandomNumber(0, 10)
    jewelry = generateRandomNumber(0, 10)
    smoke = generateRandomNumber(0, 10)
    hat = generateRandomNumber(0, 25)
    glasses = generateRandomNumber(0, 15)
    mask = generateRandomNumber(0, 35)
    special = generateRandomNumber(0, 250)

    # Feature map
    bodyMap = createBodyMap()
    eyeMap = createEyeMap()
    mouthMap = createMouthMap()
    hairMap = createHairMap()
    facialHairMap = createFacialHairMap()
    jewelryMap = createJewelryMap()
    smokeMap = createSmokeMap()
    hatMap = createHatMap()
    glassesMap = createGlassesMap()
    maskMap = createMaskMap()
    specialMap = createSpecialMap()

    # Create data object for json file creation
    # data = createDataMap(i)

    Swag = 0

    # Special characteristic - Allow smoke & jewelry only
    if(0 < special <= 2):
        img0 = Image.open("Assets/Special/" + str(special) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Special',
                'value': specialMap[special]
            })
        print('Special' + str(special))
        Swag = Swag + 80
        if(0 < smoke <= 4):
            img6 = Image.open("Assets/Smoke/" + str(smoke) + ".png")
            img0.paste(img6, (0, 0), img6)
            data['attributes'].append(
                {
                    'trait_type': 'Smoke',
                    'value': smokeMap[smoke]
                })
            Swag = Swag + 10
        else:
            smoke = 0

        if(0 < jewelry <= 5):
            img5 = Image.open("Assets/Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
                })
            if(jewelry >= 4):
                Swag = Swag + 10
            else:
                Swag = Swag + 5
    else:
        special = 0

        # Open Required pngs
        img0 = Image.open("Assets/Body/" + str(body) + ".png")
        data['attributes'].append(
            {
                'trait_type': 'Body',
                'value': bodyMap[body]
            })
        if(body > 3):
            Swag = Swag + 10
        img1 = Image.open("Assets/Eyes/" + str(eyes) + ".png")
        img2 = Image.open("Assets/Mouth/" + str(mouth) + ".png")

        # Paste Required PNGs
        img0.paste(img1, (0, 0), img1)
        data['attributes'].append(
            {
                'trait_type': 'Eyes',
                'value': eyeMap[eyes]
            })
        if(eyes == 5):
            Swag = Swag + 10
        img0.paste(img2, (0, 0), img2)
        data['attributes'].append(
            {
                'trait_type': 'Mouth',
                'value': mouthMap[mouth]
            })
        if(mouth == 7):
            Swag = Swag + 10
        # Open AND Paste Optional PNGs
        if(0 < hair <= 8):
            img3 = Image.open("Assets/Hair/" + str(hair) + ".png")
            img0.paste(img3, (0, 0), img3)
            data['attributes'].append(
                {
                    'trait_type': 'Hair',
                    'value': hairMap[hair]
                })
            if(3 < hair <= 6):
                Swag = Swag + 5
            if(hair >= 7):
                Swag = Swag + 10
        if(0 < facialHair <= 7):
            img4 = Image.open("Assets/FacialHair/" +
                              str(facialHair) + ".png")
            img0.paste(img4, (0, 0), img4)
            data['attributes'].append(
                {
                    'trait_type': 'Facial Hair',
                    'value': facialHairMap[facialHair]
                })
            if(facialHair == 7):
                Swag = Swag + 10
            if(hair == 6):
                Swag = Swag + 5
        else:
            facialHair = 0
        if(0 < jewelry <= 5):
            img5 = Image.open("Assets/Jewelry/" + str(jewelry) + ".png")
            img0.paste(img5, (0, 0), img5)
            data['attributes'].append(
                {
                    'trait_type': 'Jewelry',
                    'value': jewelryMap[jewelry]
                })
            if(jewelry >= 4):
                Swag = Swag + 10
            else:
                Swag = Swag + 5
        else:
            jewelry = 0

        # Mask - If mask, no smoke, hat or glasses added
        if(0 < mask <= 5):
            if(mask < 3 and hair != 6):
                img9 = Image.open("Assets/Mask/" + str(mask) + ".png")
                img0.paste(img9, (0, 0), img9)
                data['attributes'].append(
                    {
                        'trait_type': 'Mask',
                        'value': maskMap[mask]
                    })
            if(mask == 5):
                Swag = Swag + 25
            if(2 < mask < 5):
                Swag = Swag + 20
            if(mask <= 2):
                Swag = Swag + 10
        else:
            if(0 < smoke <= 4):
                img6 = Image.open("Assets/Smoke/" + str(smoke) + ".png")
                img0.paste(img6, (0, 0), img6)
                data['attributes'].append(
                    {
                        'trait_type': 'Smoke',
                        'value': smokeMap[smoke]
                    })
                Swag = Swag + 10
            else:
                smoke = 0
            if((0 < hat <= 4) and (hair != 6)):
                img7 = Image.open("Assets/Hat/" + str(hat) + ".png")
                img0.paste(img7, (0, 0), img7)
                data['attributes'].append(
                    {
                        'trait_type': 'Hat',
                        'value': hatMap[hat]
                    })
                if(hat == 4):
                    Swag = Swag + 10
                else:
                    Swag = Swag + 5
            else:
                hat = 0
            if(0 < glasses <= 6):
                img8 = Image.open("Assets/Glasses/" +
                                  str(glasses) + ".png")
                img0.paste(img8, (0, 0), img8)
                data['attributes'].append(
                    {
                        'trait_type': 'Glasses',
                        'value': glassesMap[glasses]
                    })
                if(glasses <= 3):
                    Swag = Swag + 10
                else:
                    Swag = Swag = 5
            else:
                glasses = 0
            mask = 0        # img0.show()
    data['attributes'].append(
        {
            'display_type': 'boost_number',
            'trait_type': 'Swag',
            'value': Swag
        })
    # Create and save data
    folder = "Assets/Homies/{}/".format(str(token_id))
    if not os.path.isdir(folder):
        os.mkdir(folder)

    # Resize image - maintain quality
    # back = Image.open("Background/backGround.png")
    # back.paste(img0, (0, 0), img0)
    resized_img = img0.resize((300, 300), resample=Image.NEAREST)
    resized_img.save(folder + str(token_id) + '.png', "PNG")

    img0.show()

    # IPFS upload
    image_to_upload = None
    meta_to_upload = None
    if os.getenv("UPLOAD_IPFS") == "true":
        image_path = folder + str(token_id) + '.png'
        meta_path = folder + str(token_id) + 'data.json'
        print('ImagePath: ' + image_path)
        # Returns the image uri
        image_to_upload = upload_to_ipfs(image_path, str(token_id) + '.png')

        # Add image to IPFS
        data['image'] = image_to_upload
        with open(folder + str(token_id) + 'data.json', 'w') as f:
            json.dump(data, f)
        # Returns the meta uri
        meta_to_upload = upload_to_ipfs(meta_path, str(token_id) + 'data.json')
    return meta_to_upload


def upload_to_ipfs(filepath, name):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"file": image_binary})
        # print("Response " + response.json())
        print("Hash " + response.json()['Hash'])
        ipfs_hash = response.json()['Hash']
        filename = filepath.split("/")[-1:][0]
        print("Filename " + filename)
        # uri = 'https://ipfs.io/ipfs/{}?filename={}'.format(ipfs_hash, filename)
        # print("URI " + uri)
        uriForOS = "ipfs://{}".format(ipfs_hash)
        print("URI " + uriForOS)
        # return uri

        #ipfs_pin_command = "ipfs pin remote add --service=Pinata {}".format(ipfs_hash)
        pin_response = requests.post(
            ipfs_url + "/api/v0/pin/remote/add?arg={}&name={}&service=Pinata".format(ipfs_hash, name))
        print(pin_response)
        return uriForOS
    return None


def createBodyMap():
    bodyMap = {
        1: 'Thin',
        2: 'Thin',
        3: 'Thin',
        4: 'Thick',
        5: 'Thick',
        6: 'Thick'
    }
    return bodyMap


def createEyeMap():
    eyeMap = {
        1: 'Normal',
        2: 'Peep',
        3: 'Squint',
        4: 'Peer',
        5: 'Gold',
    }
    return eyeMap


def createMouthMap():
    mouthMap = {
        1: 'Normal',
        2: 'Grin',
        3: 'Smile',
        4: 'Ohh',
        5: 'Lips',
        6: 'Missing Tooth',
        7: 'Gold Tooth'
    }
    return mouthMap


def createHairMap():
    hairMap = {
        1: 'Black',
        2: 'Brown',
        3: 'Gray',
        4: 'Pink',
        5: 'Comb-Over',
        6: 'Man-Bun',
        7: 'Corn-Rows',
        8: 'Mullet'
    }
    return hairMap


def createFacialHairMap():
    facialHairMap = {
        1: 'Light',
        2: 'Stuble',
        3: 'Handle-Bar Beard',
        4: 'Light Handle-Bar Beard',
        5: 'Grey Beard',
        6: 'Moustache',
        7: 'Handle-Bar'
    }
    return facialHairMap


def createJewelryMap():
    jewelryMap = {
        1: 'Gold Chain',
        2: 'Gold Chain & Earring',
        3: 'Diamond Chain',
        4: 'Diamond Chain, Earring & Nose Ring',
        5: 'XL Gold Chain & Diamond Earring'
    }
    return jewelryMap


def createSmokeMap():
    smokeMap = {
        1: 'Cigarette',
        2: 'Joint Sativa',
        3: 'Jeferey',
        4: 'Joint Indica'
    }
    return smokeMap


def createHatMap():
    hatMap = {
        1: 'Bonzai',
        2: 'Backwards Cap',
        3: 'DuRag',
        4: 'Crown'
    }
    return hatMap


def createGlassesMap():
    glassesMap = {
        1: 'Carerra',
        2: 'Miami',
        3: 'Dahmer',
        4: 'Dahmer - Dark',
        5: 'Pink Stunners',
        6: 'Patch'
    }
    return glassesMap


def createMaskMap():
    maskMap = {
        1: 'Balaklava',
        2: 'Ninja',
        3: 'Doom',
        4: 'Doom 2',
        5: 'Jason'
    }
    return maskMap


def createSpecialMap():
    specialMap = {
        1: 'Alien',
        2: 'Death'
    }
    return specialMap
