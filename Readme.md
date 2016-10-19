Dokumentasi Instalasi Server
//Untuk menginstalasi web server statis digunakan
apt-get install nginx
edit /etc/nginx/sites-available/default
Tambahkan
//location / {
root /usr/share/nginx/html;
index index.php index.html index.htm;
//Untuk mengatasi error setelah direstart tambahkan autoindex on;
//Uncomment baris berikut
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;
location = /50x.html {
	root /usr/share/nginx/html;
}
location ~ \.php$ {
	try_files $uri =404;
	fastcgi_split_path_info ^(.+\.php)(/.+)$;
 	fastcgi_pass unix:/var/run/php5-fpm.sock;
	fastcgi_index index.php;
	include fastcgi_params;
	}
//Untuk Instalasi MongoDB
apt-get install php5-cli php5-common php5-cgi php5-curl php5-fpm php5-json php5-mcrypt php5-mysql php5-sqlite php5-dev php-pear php-apc
pecl install mongo
//Mongo menggunakan Nginx
echo "extension=mongo.so" >> /etc/php5/fpm/php.ini
//Mongo Apache2
echo "extension=mongo.so" >> /etc/php5/apache2/php.ini
apt-get install mongodb mongodb-server
//Export mongodb
export LC_ALL="en_US.UTF-8"
mongodump -d ugm -o ugmbackup
//Import mongodb
mongorestore -d ugm /path/to/file
//Melihat schema mongodb
mongo ugm --eval "var collection = 'antrian' " variety.js
//Untuk Instalasi OpenCV
sudo apt-get install build-essential libgtk2.0-dev libjpeg-dev libtiff4-dev libjasper-dev libopenexr-dev cmake python-dev python-numpy python-tk libtbb-dev libeigen3-dev yasm libfaac-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev libx264-dev libqt4-dev libqt4-opengl-dev sphinx-common texlive-latex-extra libv4l-dev libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev default-jdk ant libvtk5-qt4-dev
cd ~
wget http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.9/opencv-2.4.9.zip
unzip opencv-2.4.9.zip
cd opencv-2.4.9
mkdir build
cd build
cmake -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_VTK=ON ..
make
sudo make install
sudo nano /etc/ld.so.conf.d/opencv.conf
/usr/local/lib
sudo ldconfig
sudo gedit /etc/bash.bashrc
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
export PKG_CONFIG_PATH
//Untuk melihat Flags dan Libs yang digunakan untuk kompilasi program C OpenCV
pkg-config --cflags --libs opencv
//Program untuk homomorphic filtering terdapat pada folder homo_server_revisi1
//Untuk melakukan kompilasi program tersebut
g++ main.cpp cl_Texture.cpp clcnst/clcnst.cpp -o porntest -I/usr/local/include/opencv -I/usr/local/include /usr/local/lib/libopencv_calib3d.so /usr/local/lib/libopencv_contrib.so /usr/local/lib/libopencv_core.so /usr/local/lib/libopencv_features2d.so /usr/local/lib/libopencv_flann.so /usr/local/lib/libopencv_gpu.so /usr/local/lib/libopencv_highgui.so /usr/local/lib/libopencv_imgproc.so /usr/local/lib/libopencv_legacy.so /usr/local/lib/libopencv_ml.so /usr/local/lib/libopencv_nonfree.so /usr/local/lib/libopencv_objdetect.so /usr/local/lib/libopencv_ocl.so /usr/local/lib/libopencv_photo.so /usr/local/lib/libopencv_stitching.so /usr/local/lib/libopencv_superres.so /usr/local/lib/libopencv_ts.a /usr/local/lib/libopencv_video.so /usr/local/lib/libopencv_videostab.so /usr/local/lib/libopencv_viz.so /usr/lib/x86_64-linux-gnu/libXext.so /usr/lib/x86_64-linux-gnu/libX11.so /usr/lib/x86_64-linux-gnu/libICE.so /usr/lib/x86_64-linux-gnu/libSM.so /usr/lib/x86_64-linux-gnu/libGL.so /usr/lib/x86_64-linux-gnu/libGLU.so -ltbb -lrt -lpthread -lm -ldl
//Untuk Proxy Server
apt-get install squid3
//Untuk Tuning Konfigurasi Squid
sudo nano /etc/squid3/squid.conf
//Berikut merupakan konfigurasi dasar squid3
http_port 3030
#access allow
acl all src
acl semua src all
http_access allow all
redirect_program /usr/bin/python /home/me/serverfinal.py
cache deny all
cache_dir null /tmp
#access_log /var/log/squid3/access.log
//Program yang dibutuhkan di server
File serverfinal.py merupakan file yang digunakan untuk rewrite URL dari database
selain itu file ini juga akan melakukan insert data baru ke database
File crontabfinal.sh merupakan script yang berjalan di background
agar bisa memanggil script downloadfinal.py setiap statustemp adalah 1
File downloadfinal ini berfungsi untuk memanggil program penapis teks dengan nama text-filtering.py
dan memanggil program penapis citra python pija.py dan ./porntest untuk penapis citra C++
setelah diterapkan algoritma fusi maka hasil replace akan disimpan di database dan akan direload
pada saat script serverfinal.py mengecek URL pengguna dengan URL di database
//Program Penapis Teks
Program penapis ini terdiri dari
text-filtering.py
folder model untuk menyimpan model hasil training
folder res untuk menyimpan dictionary
folder resource untuk menyimpan dataset training
folder util untuk file sorter.py
//Program Penapis Citra Python
Program penapis ini terdiri dari
pija.py
file analizer.py digunakan untuk melakukan deteksi citra
file key_frame_extractor untuk mengekstraksi video (belum digunakan)
file shape.dat merupakan hasil training wajah yang perlu disimpan dan disesuaikan foldernya pada file analizer.py
//Third Party Library untuk Citra
OpenCV dan Dlib
Dlib harus dikompilasi terlebih dahulu untuk mendapatkan file dlib.so untuk Linux
Buka folder python_examples kemudian jalankan ./compile_dlib_python_module.bat
//Monitoring Data
File di dalam folder data merupakan API yang digunakan PHP untuk mengakses data dari MongoDB sehingga bisa dilihat
list antrian database dan juga view yang lain
File data harus dicopy ke folder
//Nginx
/usr/share/nginx/html
//Apache2
/var/www/html
//File Demo GUI Penapis
File demo GUI ini menggunakan Django untuk Web Interactionnya
virtualenv diperlukan untuk membuat environment khusus development ini
File package terdapat pada file requirements.txt
//Instalasi Package
//Aktifkan virtualenv
source bin/activate
pip install -i requirements.txt
File views atau template pada Django harus menyesuaikan webserver yang dipakai
karena direktorinya berbeda
//Running Django development
Seluruh file proyek Django terdapat pada file pornfilterfinal.zip
Ketika pertama kali mencoba Django cari folder di mana manage.py berada
Untuk mencoba apakah instalasi package sudah benar
maka bisa melakukan perintah
python manage.py runserver untuk melakukan testing apakah program Django bisa berjalan
Bila sudah berjalan dan ingin running di background
maka bisa menggunakan gunicorn untuk melayani web dinamis dan Nginx untuk file statisnya
Bila menggunakan gunicorn dan nginx maka file staticnya harus disesuaikan letaknya
Agar file static bisa diakses dari nginx maka konfigurasi harus ditambahkan ke /etc/nginx/sites-enabled/default
        location /static {
                autoindex on;
                root /path/to/static/root;
                allow all;
        }
Perintah untuk menjalankan gunicorn adalah
gunicorn /path/to/wsgi/folder.wsgi:application -b 0:port -t timeout