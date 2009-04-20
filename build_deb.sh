VERSION="0.1"
cd debs
svn co http://desigle.googlecode.com/svn/trunk/ desigle
cd desigle
VERSION="${VERSION}_r`svnversion .`"
rm -Rf debs debian
find .svn | xargs rm -Rf
cd ..
mv desigle desigle-$VERSION
tar -czvvf desigle-$VERSION.tar.gz desigle-$VERSION
cd desigle-$VERSION
#dh_make -e public@kered.org -c GPL -f ../desigle-$VERSION.tar.gz 
cp -R ../../debian .
rm -Rf debian/.svn
echo "desigle ($VERSION-1) unstable; urgency=low" > debian/changelog
fakeroot debian/rules binary
cd ..
rm -Rf desigle-$VERSION
rm desigle-$VERSION.tar.gz
svn add desigle_${VERSION}-1_all.deb

