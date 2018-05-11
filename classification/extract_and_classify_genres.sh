echo "Extracting classical features"
python3 feature_extraction.py --label=0 ../graphdata/classical/*

echo "Extracting jazz features"
python3 feature_extraction.py --label=1 ../graphdata/jazz/*

echo "Classifying"
python3 classify.py
