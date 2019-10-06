# AngelCS Machine Learning


## Requirements
Python 3.6 이상<br>
Jupyter Notebook 기반의 코드들입니다.<br>
사용 라이브러리: Tensorflow, Keras, Numpy, Pandas, TextBlob, NLTK

Tensorflow-gpu를 사용하려면 CUDA가 설치되어야 합니다. [CUDA 관련글](https://towardsdatascience.com/installing-tensorflow-with-cuda-cudnn-and-gpu-support-on-windows-10-60693e46e781)

## 프로젝트 구조
| 디렉토리 | 용도 |
|---|---|
| raw/ | 학습에 사용되는 데이터의 원본 저장되는 디렉토리 |
| data/ | raw/에 있는 원본 데이터를 가공하여 저장하는 디렉토리 |
| preprocessing/ | raw데이터를 바탕으로 dataset을 가공하여 data/ 에 저장하는 전처리 IPython 코드들이 들어있는 디렉터리 |
| learning/ | data/에 있는 가공된 데이터를 바탕으로 학습을 수행하는 IPython코드가 존재하는 디렉터리. |
| model/ | 학습이 수행된 후 만들어진 모델을 저장하는 디렉터리.|
| api | IPython코드들을 정리하여 실행가능한 API로 구현된 코드들이 저장된 패키지. model/ 디렉터리의 모델들을 사용함. |

raw, data, model 디렉토리는 gitignore에 포함되어있습니다. Dataset에 있는 정보를 바탕으로 직접 다운로드한 후 학습하셔야 합니다.

## 머신러닝 프로세스
1. 데이터셋을 다운로드받아서 raw/ 에 저장
2. preprocessing의 전처리 노트북을 실행해서 가공 후 data/ 디렉토리에 저장.
3. learning/ 의 노트북으로 학습을 수행해서 모델을 model/ 에 저장
4. 앞서 노트북으로 구현한 코드들을 정리해서 api/에 모듈화.


## Dataset
| 이름 | 단체 | 링크 |
|---|---|---|
| Consumer Reviews of Amazon Products | Amazon | https://www.kaggle.com/datafiniti/consumer-reviews-of-amazon-products |
| Dataset for Detection of Cyber-Trolls | Dataturks | https://dataturks.com/projects/abhishek.narayanan/Dataset%20for%20Detection%20of%20Cyber-Trolls
| SQUAD 2.0 | Stanford University | https://rajpurkar.github.io/SQuAD-explorer/ |



## Reference
1. Text classification with preprocessed text: Movie reviews, Google, https://www.tensorflow.org/tutorials/keras/text_classification