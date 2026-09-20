#!/usr/bin/env python3
"""Build a debug APK from checked-in UI assets using the official Android SDK.
Usage: python3 build_apk.py --sdk /path/to/android-sdk
Java 17, platform android-35, and build-tools 35.0.0 are required.
"""
from pathlib import Path
import subprocess,os,argparse,zipfile
p=argparse.ArgumentParser();p.add_argument('--sdk',default=os.getenv('ANDROID_HOME') or os.getenv('ANDROID_SDK_ROOT'));p.add_argument('--keystore');a=p.parse_args()
if not a.sdk:p.error('Pass --sdk or set ANDROID_HOME')
root=Path(__file__).resolve().parent;sdk=Path(a.sdk);tools=sdk/'build-tools/35.0.0';jar=sdk/'platforms/android-35/android.jar';out=root/'build';out.mkdir(exist_ok=True)
for name in ['generated','classes','dex']:(out/name).mkdir(exist_ok=True)
def run(*args):subprocess.run([str(x) for x in args],check=True,cwd=root)
run(tools/'aapt2','compile','--dir',root/'app/src/main/res','-o',out/'resources.zip')
run(tools/'aapt2','link','-o',out/'unsigned.apk','--manifest',root/'app/src/main/AndroidManifest.xml','-I',jar,'--java',out/'generated','-A',root/'app/src/main/assets','--auto-add-overlay',out/'resources.zip')
sources=list((root/'app/src/main/java').rglob('*.java'))+list((out/'generated').rglob('*.java'))
run('java','com.sun.tools.javac.Main','--release','17','-cp',jar,'-d',out/'classes',*sources)
run(tools/'d8','--min-api','26','--lib',jar,'--output',out/'dex',*list((out/'classes').rglob('*.class')))
with zipfile.ZipFile(out/'unsigned.apk','a',zipfile.ZIP_DEFLATED) as z:
 for f in (out/'dex').glob('*.dex'):z.write(f,f.name)
run(tools/'zipalign','-f','4',out/'unsigned.apk',out/'aligned.apk')
key=Path(a.keystore) if a.keystore else out/'debug.keystore'
if not key.exists():run('keytool','-genkeypair','-keystore',key,'-storepass','android','-keypass','android','-alias','androiddebugkey','-dname','CN=Android Debug,O=Android,C=US','-keyalg','RSA','-keysize','2048','-validity','10000')
run(tools/'apksigner','sign','--ks',key,'--ks-pass','pass:android','--key-pass','pass:android','--out',out/'Doseleaf-Android-Preview.apk',out/'aligned.apk')
run(tools/'apksigner','verify','--verbose',out/'Doseleaf-Android-Preview.apk')
print('APK:',out/'Doseleaf-Android-Preview.apk')
