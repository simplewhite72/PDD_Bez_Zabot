def check_question(input_text:str, df):
    output = dict()
    output['video_file_id'] = "Type_Error"
    output['caption'] = ''
    output['title'] = ''
    output['thumb'] = ''
    if (len(input_text) != 4) or input_text.isdigit() == False :
        output['video_file_id'] = "Type_Error"
    elif int(input_text) <= 4020 :
        bilet_num = int(input_text[0:2])
        question_num = int(input_text[2:4])
        if (bilet_num>40) or (bilet_num==0) :
            output['video_file_id'] = "Type_Error"
        elif (question_num>20) or (question_num==0) :
            output['video_file_id'] = "Type_Error"
        else :
            temp_str = df.loc[(df['paper_id'] == bilet_num) & (df['paper_order'] == question_num)]
            temp_str = temp_str.reset_index()
            output['video_file_id'] = str(temp_str['video_file_id'].iloc[0])
            output['caption'] = str(temp_str['caption'].iloc[0])
            output['title'] = str(temp_str['title'].iloc[0])
            output['thumb'] = str(temp_str['thumb'].iloc[0])
    else :
        output['video_file_id'] = "Type_Error"
    return output       