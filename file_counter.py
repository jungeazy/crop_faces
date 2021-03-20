import sys
import glob

relevant_emotions = ['angry', 'fear', 'happy', 'sad', 'surprise']
excluded_emotions = ['disgust', 'neutral']

if sys.argv[3] in relevant_emotions:
    old_feeling = sys.argv[1]
    rule = sys.argv[2]
    new_feeling = sys.argv[3]
    confidence = sys.argv[4]
    file_list = glob.glob('{}/{}/{}/cropped_{}to*.jpg'.format(rule, confidence, new_feeling, old_feeling))
    print('Under {}, {} images were sorted from {} to {} with {} confidence.'.format(rule, len(file_list), old_feeling, new_feeling, confidence))

elif sys.argv[3] in excluded_emotions:
    old_feeling = sys.argv[1]
    rule = sys.argv[2]
    new_feeling = sys.argv[3]
    file_list = glob.glob('{}/discard/cropped_{}to{}*.jpg'.format(rule, old_feeling, new_feeling))
    print('Under {}, {} images were sorted from {} to {}.'.format(rule, len(file_list), old_feeling, new_feeling))

elif sys.argv[3] == 'same_score':
    old_feeling = sys.argv[1]
    rule = sys.argv[2]
    new_feeling = sys.argv[3]
    file_list = glob.glob('{}/{}/cropped_{}to*.jpg'.format(rule, new_feeling, old_feeling))
    print('Under {}, {} {} images were classified with at least the first two emotions having equal percentages.'.format(rule, len(file_list), old_feeling))

elif sys.argv[3] == 'none':
    old_feeling = sys.argv[1]
    rule = sys.argv[2]
    new_feeling = sys.argv[3]
    file_list = glob.glob('{}/discard/cropped_{}to{}*.jpg'.format(rule, old_feeling, new_feeling))
    print('Under {}, {} {} images are unclassified.'.format(rule, len(file_list), old_feeling))

else:
    print('Invalid arguments, please try again.')
