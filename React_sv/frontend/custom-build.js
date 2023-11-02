const fs = require('fs');
const rimraf = require('rimraf');
const path = require('path');

// Đường dẫn đến thư mục `build` trong thư mục frontend
const sourceDirectory = path.join(__dirname, 'C:/REDDOT/Call_API_App/React_sv/frontend/build');

// Đường dẫn đến thư mục `build` trong thư mục Call_API_App
const destinationDirectory = path.join(__dirname, 'C:/REDDOT/Call_API_App/build');

// Xóa thư mục `build` cũ trong thư mục Call_API_App
rimraf(destinationDirectory, (error) => {
  if (error) {
    console.error('Xóa thư mục build cũ không thành công:', error);
  } else {
    console.log('Đã xóa thư mục build cũ thành công.');
    
    // Sao chép thư mục `build` mới từ thư mục frontend vào thư mục Call_API_App
    fs.mkdirSync(destinationDirectory, { recursive: true });
    fs.readdirSync(sourceDirectory).forEach((file) => {
      const sourceFile = path.join(sourceDirectory, file);
      const destinationFile = path.join(destinationDirectory, file);
      fs.copyFileSync(sourceFile, destinationFile);
    });
    
    console.log('Đã sao chép thư mục build mới thành công.');
  }
});
