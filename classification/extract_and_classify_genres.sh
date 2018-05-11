echo "Extracting classical features"
python3 feature_extraction.py --label=0 --train ../graphdata/classical/*

echo "Extracting jazz features"
python3 feature_extraction.py --label=1 --train ../graphdata/jazz/*

echo "Extracting classical test features"
python3 feature_extraction.py --label=0 ../graphdata/classicaltest/*

echo "Extracting jazz test features"
python3 feature_extraction.py --label=1 ../graphdata/jazztest/*

echo "Classifying and testing"
python3 classify.py
