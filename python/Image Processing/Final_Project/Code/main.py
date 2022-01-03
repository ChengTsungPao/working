from Show_Result import show_result

if __name__ == "__main__":

    path = "./Scaphoid/"
    show_result_fcn = show_result(path)

    for index in range(120):
        IOU, recall, precision, f1_score = show_result_fcn.all_bounding_box_wider_data_evaluation[index]
        print("IOU = {}, recall = {}, precision = {}, f1_score = {}".format(IOU, recall, precision, f1_score))
        show_result_fcn.predict_bounding_box_wider_data(index)

        IOU, recall, precision, f1_score = show_result_fcn.all_bounding_box_narrow_data_evaluation[index]
        print("IOU = {}, recall = {}, precision = {}, f1_score = {}".format(IOU, recall, precision, f1_score))
        show_result_fcn.predict_bounding_box_narrow_data(index)

        show_result_fcn.predict_classifier_data(index)
