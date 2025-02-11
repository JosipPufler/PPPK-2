import os

from scripts import downloadFromBucket, joinMongoAndPatientData, processDataAndUploadToMongoDB, visualize, \
    uploadToBucket


def main():
    while True:
        print("Enter command:")
        command = input()
        match command.lower():
            case "exit":
                return
            case "clear":
                if os.name == 'nt':
                    _ = os.system('cls')
                else:
                    _ = os.system('clear')
            case "info":
                print("1: upload to bucket")
                print("-Uploads all .tsv files from folder to a MinIO bucket")
                print("2: download from bucket")
                print("-Downloads all .tsv files from MinIO bucket")
                print("3: process to mongo")
                print("-Combines and processes downloaded .tsv files and uploads to MongoDB cluster")
                print("4: join mongo with patients")
                print("-Joins data from MongoDB cluster with a .tsv containing patient data")
                print("5: visualize")
                print("-Creates visualization of (some) patient data")
            case "upload to bucket":
                uploadToBucket.run()
            case "download from bucket":
                downloadFromBucket.run()
            case "process to mongo":
                processDataAndUploadToMongoDB.run()
            case "join mongo with patients":
                joinMongoAndPatientData.run()
            case "visualize":
                visualize.run()
            case "1":
                uploadToBucket.run()
            case "2":
                downloadFromBucket.run()
            case "3":
                processDataAndUploadToMongoDB.run()
            case "4":
                joinMongoAndPatientData.run()
            case "5":
                visualize.run()
            case _:
                print("Invalid command")

if __name__ == '__main__':
    main()