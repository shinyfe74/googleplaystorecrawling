import time
import glob
import os
import re
import pandas as pd


### CSV 파일 합치기 함수
def combine_file(file_name):
    input_path = "./data"  # CSV 파일 디렉토리 경로
    output_file = "./data/" + file_name + ".csv"  # CSV 저장 파일명

    all_file_lst = glob.glob(os.path.join(input_path,
                                          "cmt_*"))  # cmt_로 시작하는 모든 CSV 파일

    all_data_lst = []  # 임시 저장용 빈 리스트
    for f_name in all_file_lst:
        df_temp = pd.read_csv(f_name)
        all_data_lst.append(df_temp)  # 매 Loop에서 획득한 DataFrame을 임시 리스트에 적재r

    data_combine = pd.concat(all_data_lst, axis=0,
                             ignore_index=True)  # 임시 리스트 속 DataFame을 일괄 병합
    data_combine.index = data_combine.index + 1
    data_combine.to_csv(output_file, encoding="utf-8-sig",
                        index=True)  # CSV 파일로 저장


combine_file("cmt_google_app")
