import logging

import azure.functions as func
import os
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import re
import base64
import datetime
import json


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    imagePayload = '%2F9j%2F4AAQSkZJRgABAQEAAAAAAAD%2F2wBDAAoHCAkIBgoJCAkLCwoMDxkQDw4ODx8WFxIZJCAmJiQgIyIoLToxKCs2KyIjMkQzNjs9QEFAJzBHTEY%2FSzo%2FQD7%2F2wBDAQsLCw8NDx0QEB0%2BKSMpPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj4%2BPj7%2FxAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv%2FxAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4eLj5OXm5%2Bjp6vHy8%2FT19vf4%2Bfr%2FxAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv%2FxAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4%2BTl5ufo6ery8%2FT19vf4%2Bfr%2FwAARCADwAUADASEAAhEBAxEB%2F9oADAMBAAIRAxEAPwDE8hc5xSCFM%2FcobDkVxxhjP8P5U4QR5%2B5THyD%2FACI8fcpPIi%2FufrSQvZxF8iPP%2BrFHkRdkAqubQOWLDyYs%2FwCrFL5UXeMVPMHIhDBD%2FwA81pphjPVBRfuHKrh5EWP9UtHkw5%2F1YqnLQOUb5Ef9xaTyoy3%2BrFSgUEM8iPP3KQwRAY8v9TTuNRRG0K%2F3aTy0x%2FqxV2VgcIjDEvpTTCv939aU7FctiPyl7LimlBT5hciIzGo6CmbOapaonkQ0qKZioE0huBTSvpSeghpFNxSuAzn0ooENxScClshXGmmd%2BBTWwdA4NNxSGd3jninAUNmjE21IKfkPmFpMetLYVx1JQIKKegCEUhFABSUDENN4FMQn4UlGwXGfWmle1MvmG9ulRsKXUBm35aZ2ppjdiJhUZpiY1qiNNJE2GnGOBio6RL0EOPSmH6VOwuo3PrQaTENph96YhtJUgN6UVYHe4p1Q0aXuFOosACiiwAKKLah1EpaEMQ0VVhCUnekHkBpmKYB1pNtSAwiigZGaay1Q0yMrTCKkq2pGy4qJh6VV2xETUw1RLI6ZUksZ1NNP6UEjaaaTDcQ0ykFxCKbVdA6CGm0tguehkUlIsUU6hjENFMTDFJSAWkIoiAUYoAQ0ho1ANtJin0GhKSgVhtMxikh2EIpjLxWlwsN21Gy8VK3K5%2BhHiosccigoiIqMinuBGRz0qI9aDOQ00w0iWNprUmQNptBTG0hFK9hbjTTaLgei0AUbFXYd6WgYY5ooABSY5oAKKECDFFMOoYpuOevbpSuAnakxT6ALtppFAEdJVaDExSUmO43FMIqdbiIzUbLTAhIqNh2pjRCQajcCmh2I260w0TZGpGe9MPSpJfcaaSixI1hTTQMaRTTQ2JanpBopGgUvWhiEoxRcQUUxhRSGFGKYISkxSGFGKYCYpppdRDaaRTHuN70hHFIVhppuKoZERTT0pjI2WoT7ipHYiqFqaC5Ew5phFEiWRkU00XsQxhplAridaaai%2FQQ002qKjbc9HxS0Mph3paAEpaVwCkoC4tFACYopgFJSGFFMQ2kIpXGIRTaYXG0lDAb3pppCGEVGRmmV5kbcKahagOYiaoiPQUBchaoqqwbjDTGFBL3IjSGpvqQNptJgNptPoFj0k8dqWpLEpTVEiUtIoKKACigQd6KLlXCkxQIKKBiU2gYhpuOKBDcUmKYhlNNAxpqM0AyM1Ey8UgImFQsA3UUxkLDFRGriBGaYeKRIw0w1PUkZSH6UiRhptVYZ6WaKksSloEFFAwpaACloASipGJRincApKYBTaBhjimnpQxDMUlMGMNNNIGMPWmmqYyI0w1JJEahaiw%2BpAwqFhVbFER60w9KCCLNI1LqSR0HrS6kkbdabVRK3PS6BUFC0UxBRQxhS0AGKWgBKKACjFACYoo3AKb3pFCUhpiGmmGmAhqOmA2mEUikiOoyKCWRnrUL0McSFsfjULUhvYhIxUbCtLisMYYqOs%2FMzYxqYaEIbSGqQj0uipLClo3GGKKAFxRSAKKYBRSAKKYBSd6BhSYpDG0lOwCU00iRlMNMoYaZQAw1E1PclMjNRNTehRC1QvUjuQtUbVQSImqM0mjJsaaZ3qegDab9ad7AemU0UDFpaBhS4oYBRSAWimAUUDCkoEFFBQUlIkaaQ0wQykPWgY2mGmCG1GaQ7DDUZoJ2IzUTCmymQtUDUh3ImqFqphYiNR0GbGHrTam5I2m0WuCPTKKCwpaBJBRSAWk70xi0UALiigYUlABSUAFJjmgBKSiwDTTSKLiG000gIzTDTGxlRmgRG1RN900IZF2qBqCkQtUL0AQmmGqIGU2pMxmKaRQNHplLQWFFAgpaBhS0AgpaAsFFACUUDEooGFJQISkp3AaabSAaaZQAw0w0AyNqYaYiN6gagojbioWFDQEDVE1UNkL1GaRG5HTT1qSBDTKOgj000CgsKKBhS0ALRQAtFCAKKHqAUUDEooASkoF1EpDQMaaSgBhpho0BEZFMpgMqM0gIzUTU2IjfrUD07oIkJ96hajqUQmozQS0MNMpGYw0hoY0uh6bRSL6hRSAWloAKKAFopgLRQAUlAwpKACkpAJSUwGGkouDGU00AMNRmgCM1GaBjGqI0CZE1QtQ2Mhb2qBqaGRnpURqiGRtTKiRDGmo6cQT1PT%2BoopNFXvsAp1AxKWgApaACigBaUUgEopjEooASkNIBKSmA0000hjDTTTYiM0xqEUR0w0C2ImqOqJ8yI8GoWqWUQNUT0xkTVEaNybEZqPvR0IY00hpIEem0UDCnUDEpaAFopXAWimAUUAFFIBKSgYUlMdhKSkwG000AMphpgNNRmgCM9aY1C3ERNUVAERqI0AiFqiamUQmoj1oERGm0jMZTaYj1Cm0iwpaAFooAWigAooAWikAUlAwpKLAJSUABptNDG0lFgIzTTQKww1GTQAxqjJ4oERNUdMdyJqhaluCImqE0xkTVCaaQhhqM1NiRKYaBHp5pKBgKWgApaBhS0MLBRQgCigYUUAFNoADSGgBKSgBlNpjG5phpMQw0xqBkTVGTTJGE1C1AEbe9QuaQEJqJzVW1AhNRGhjYw0zNSZDDSU72KPT6SkMWikMKKYC0UALRQAlFAC0lACUlAwpKAEpppDENMpiGGmZpgMprUgIjTDQK5E1RGn0He5G3NQt0pIEQGo26Ux2ImqFqoljDTKkgbTaVhnqGKSmMUUUDCjNIBaSgApaYBRSASimAlFIAptACU2gBpNNzTKGGmNQShlRk0DGGozTEQk1GTxQwuRPUb1NhohNQ7srTSGRkiojVEDDTalkDDTaOhR6gaKLAFFIAooZQUlAC0UAFFACUUDCkoADTaBDabTGIaYaAGk0xqBDDUZoGMzUbUbARVG1IRAxqJqBojNQmncoiOKjNMi4w001NiRtNNMD1A0UmxsSloATvRQAUtABSZoGFFABSUAFJQA2kplCU3tSJG5phoGMphaquA01ETUoQxjUZp3C5G1QmgCN6hY0uo0RE1G1UBCaZQSxhppNSSNpppAeo0UyxKWgQlFMAopdRhRTEFJSGJRmmAlJSASkp3GNptMQwmm0DGZ9KYaQDTUZovYRG3JqNqLgRGmZouNEL1C1FyiImozRcTIzUZqiBpplQmSJTaYHqOOKSkMKWgYlFAwoosISk70DFpKAEpDTASkpAITTaLDG5ptADWppqhDDTKQDCajNIYyo2p9RXIm4FRNQOJExqEk0JFETdaYTTtchkZpho2JYw0lTYQ0000Ia1PU6SgYlFABRQAUhpgFJSAKbQMKSgBDTaAEppoAaabVDGmkzSCww1GaQhlRtTGMPSozSuJWI2qE0DIT1qM0x3Is0xqZAyozQFxtNNSTYbSUhnqZoqgEpKACkoAKO9IYlFMBtFAxtJQITNNzTGJTaAGUhoAaTTCaYxrGmE0hEZ603dQBE1Mo6DsRMaiY1IiM1CaYyLvTWqiRlMNITGEU00iUJTaZR6pRSYCUlIAopgJSUMANNoASkoGhtJTGNzSUxoTvTc1AhpppqkwGH1ppNV5ghm6mEipCwyoyaQdSNqZQmPciNRNQMjaojVCIzUZNBI09aYaVxCGm1JI2m0x2PVaBTKEoNAhKKQDaKBjaSmAhpKbENpKQxuaTNIY3NMNMBuaQmgBpNRmkAwmmHiqAaeajY81OgWIzUTe1AxhNRE07CI2NRVVhjCaZSZAym1IhtNNKwhtJmqaGf%2FZ'

    deviceID = 'ISHJCU67'
    '''
    replacing “%2B” for “+” and “%2F” for “/” using Regex
    '''
    pattern = re.compile(r'%2F')
    imagePayloadFixed = pattern.sub(r'/', imagePayload)
    patternB = re.compile(r'%2B')
    imagePayloadFixed = patternB.sub(r'+', imagePayloadFixed)

    '''
        decoding
    '''

    imgdata = base64.b64decode(imagePayloadFixed)

    presentTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    connect_str = "DefaultEndpointsProtocol=https;AccountName=storeageaccountteamcbn;AccountKey=Ehc1pb8txcuLn3pgJ4LuzIqDBEZJyZA7lVsMl8c8BTQ9e1wuXx9HtKrqHR8Mf63hduufeYCWJA9199Ebo7/vFg==;EndpointSuffix=core.windows.net"

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Create a unique name for the container
    container_name = "pictures"

    container = ContainerClient.from_connection_string(
        connect_str, container_name)

    # testing if the container exists or not
    try:
        container_properties = container.get_container_properties()
        # Container foo exists. You can now use it.
        print("it does exist mOda")

    except Exception as e:
        # Container foo does not exist. You can now create it.
        container_client = blob_service_client.create_container(container_name)

    local_file_name = deviceID + "/" + presentTime + ".jpg"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=local_file_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
    blob_client.upload_blob(imgdata)
