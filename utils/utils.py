from enum import Enum


class PostprocessingMethod(Enum):
    deterministic = 'deterministic'
    non_deterministic = 'non_deterministic'

    def __str__(self):
        return self.value


class AnswerMode(Enum):
    single = 'single'
    multiple = 'multiple'

    def __str__(self):
        return self.value


help_messages = {
    'model': 'Path to the model configuration file (.cfg)',
    'weights': 'Path to the weights file (.weights or .pth)',
    'images': 'Path to the directory containing the images for question answering',
    'questions': 'Path to the file containing questions (.json)',
    'img_size': 'Image input size for YOLOv3. Non-square images are padded to obtain dimension (img_size x img_size)',
    'facts_out': 'Path to the file containing facts extracted from images. If there is no file with the given '
                 'name a new one with the same name will be created.',
    'facts': 'Path to the file containing facts extracted from images.',
    'results_out': 'Path to the location where .txt file containing the results of a run is stored',
    'bounding_box_thres': 'Confidence threshold used by YOLOv3 during object detection',
    'nms_thres': 'Non-maximum-suppression threshold used by YOLOv3 during object detection',
    'alpha': 'Number representing the factor to multiply the confidence standard deviation with to obtain '
                 'the postprocessing threshold for enhanced postprocessing',
    'k': 'Number of classes used if no class score surpasses the postprocessing threshold',
    'postprocessing_method': 'Specifies the processing method used by the scene parser to produce ASP facts',
    'answer_mode': 'Specifies the method used to select an answer from answer sets. Single makes the system pick '
                   'the highest scoring answer, while multiple selects all answers',
    'batch_size': 'Batch size used by dataloader',
    'n_cpu': 'Number of cpus used by dataloader'
}

# def get_stats(total, correct, wrong, invalid):
#    return_val = ''
#
#    correct_rel = correct / total * 100
#    wrong_rel = wrong / total * 100
#    invalid_rel = invalid / total * 100
#
#    return_val += "Questions total: \t{:7d}\n".format(total)
#    return_val += "Questions correct: \t{:7d} ({:4.2f}%)\n".format(correct, correct_rel)
#    return_val += "Questions wrong: \t{:7d} ({:4.2f}%)\n".format(wrong, wrong_rel)
#    return_val += "Questions invalid: \t{:7d} ({:4.2f}%)\n".format(invalid, invalid_rel)
#
#    return return_val


# def print_question_info(q_id, q_natural, q_true_ans, q_given_ans, q_family_id):
#    print('Image ID: {}'.format(str(q_id)))
#    print('Question: {}'.format(str(q_natural)))
#    print('Question family ID: {}'.format(str(q_family_id)))
#    print('Expected Answer: {}'.format(str(q_true_ans)))
#    print('Given Answer: {}\n'.format(str(q_given_ans)))
