hash=`git rev-parse HEAD`
echo $hash
echo $BUILD_ID
docker build . -t cglense:$hash
docker tag cglense:$hash containerregistry1z.azurecr.io/cglense:$hash
docker tag containerregistry1z.azurecr.io/cglense:$hash containerregistry1z.azurecr.io/cglense:$BUILD_ID
echo $D_PASSWORD | docker login containerregistry1z.azurecr.io -u $D_USERNAME --password-stdin
docker push containerregistry1z.azurecr.io/cglense:$BUILD_ID
