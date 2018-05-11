echo "Extracting Bach features"
python3 feature_extraction.py --label=0 ../graphdata/bach/*

echo "Extracting Chopin features"
python3 feature_extraction.py --label=1 ../graphdata/chopin/*

echo "Classifying"
python3 classify.py
