udo mkdir xmls
FILES=./*

for f in FILES;
do
sudo mv $f xmls/;
cd temp/;
sudo unzip $f;
sudo rm -rf text_000/;
sudo rm -rf native_000/;
cd ..;
done

