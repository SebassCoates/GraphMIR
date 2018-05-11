echo "Extracting Bach features"
python3 feature_extraction.py --label=0 --train ../graphdata/bach/*

echo "Extracting Chopin features"
python3 feature_extraction.py --label=1 --train  ../graphdata/chopin/*

echo "Extracting Bach test features"
python3 feature_extraction.py --label=0 ../graphdata/bachtest/*

echo "Extracting Chopin test features"
python3 feature_extraction.py --label=1  ../graphdata/chopintest/*

#echo "Classifying"
#python3 classify.py

echo "Testing"
python3 test_model.py
