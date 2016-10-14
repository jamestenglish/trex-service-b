nose2 --plugin nose2.plugins.junitxml --junit-xml
mkdir results
mv nose2-junit.xml results
cat results/nose2-junit.xml
