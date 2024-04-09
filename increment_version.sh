version=$(cat version.txt)
version=${version%.*}.$((${version##*.}+1))
echo $version > version.txt
