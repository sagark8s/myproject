hash=`git rev-parse HEAD`
echo $hash
echo $BUILD_ID
docker build . -t admin-ui:$hash
docker tag admin-ui:$hash arytic.azurecr.io/admin-ui:$hash
docker tag arytic.azurecr.io/admin-ui:$hash arytic.azurecr.io/admin-ui:$BUILD_ID
echo $D_PASSWORD | docker login arytic.azurecr.io -u $D_USERNAME --password-stdin
docker push arytic.azurecr.io/admin-ui:$BUILD_ID