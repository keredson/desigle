VERSION="0.1"
cd debs
svn export http://desigle.googlecode.com/svn/trunk/ desigle-$VERSION
tar -czvvf desigle-$VERSION.tar.gz desigle-$VERSION
cd desigle-$VERSION
#dh_make -e public@kered.org -c GPL -f ../desigle-$VERSION.tar.gz 
cp -R ../../debian .
fakeroot debian/rules binary
cd ..
rm -R desigle-$VERSION
rm desigle-$VERSION.tar.gz
svn add debs/*.deb

