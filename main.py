from Module import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filepath",
                    default=None,
                    help="Directory path where the videos are located.")
parser.add_argument("--frame",
                    default = 15,
                    help = "Frame rate for extraction.")
parser.add_argument("--height",
                    default = 224)
parser.add_argument("--width",
                    default = 224)
# parser.add_argument("--savepath",
#                     default="./",
#                     help="Data storage path")
parser.add_argument("--label",
                    default = None,
                    help="If you want to extract data and labels together, please provide the file path where the data and labels are stored in a CSV file."
                         "The columns in the CSV file should be ('video_name', 'label').")
parser.add_argument("--segment",
                    default = False,
                    help="")
parser.add_argument("--face",
                    default = False,
                    help="If you want to extract faces from the frames, specify the value as True. (Caution) If faces are not extracted, full shots will be extracted.")
args = parser.parse_args()


def main(args):
    print(args)
    # if args.label is not None:
    #     print('develop')
        
    # else:
    print('Start')
    extract_frame.extract_frame(filePath = args.filepath, frame_rate = args.frame,
                                    height = args.height, width = args.width)
        

if __name__ == '__main__':
    main(args)