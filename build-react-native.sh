

output_ios="./output/"$1"/ios"
output_android="./output/$1/android"

echo $output_android

mkdir -p $output_ios
mkdir -p $output_android

react-native bundle --dev false --entry-file index.ios.js --bundle-output $output_ios/main.jsbundle --platform ios --assets-dest $output_ios
echo ">> Build ios done"

react-native bundle --dev false --entry-file index.android.js --bundle-output $output_android/main.jsbundle --platform android --assets-dest $output_android
echo ">> Build android done"

cp -R fonts $output_ios/
cp -R fonts $output_android/

echo "Done building resources"