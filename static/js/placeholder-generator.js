// صورة مؤقتة للعرض
const canvas = document.createElement('canvas');
canvas.width = 800;
canvas.height = 600;
const ctx = canvas.getContext('2d');

// خلفية
ctx.fillStyle = '#f8f9fa';
ctx.fillRect(0, 0, canvas.width, canvas.height);

// عنوان
ctx.fillStyle = '#e74c3c';
ctx.font = 'bold 40px Cairo, sans-serif';
ctx.textAlign = 'center';
ctx.fillText('شن نطيبلك يا سالم', canvas.width / 2, 100);

// وصف
ctx.fillStyle = '#333';
ctx.font = '20px Cairo, sans-serif';
ctx.fillText('موقعك المفضل لاكتشاف وصفات طعام رائعة', canvas.width / 2, 150);
ctx.fillText('باستخدام المكونات المتوفرة لديك', canvas.width / 2, 180);

// رسم بطاقات الوصفات
function drawRecipeCard(x, y, title) {
  // بطاقة
  ctx.fillStyle = '#fff';
  ctx.shadowColor = 'rgba(0, 0, 0, 0.1)';
  ctx.shadowBlur = 10;
  ctx.shadowOffsetX = 0;
  ctx.shadowOffsetY = 4;
  ctx.fillRect(x, y, 220, 280);
  ctx.shadowBlur = 0;
  
  // صورة الوصفة
  ctx.fillStyle = '#ddd';
  ctx.fillRect(x + 10, y + 10, 200, 140);
  
  // عنوان الوصفة
  ctx.fillStyle = '#e74c3c';
  ctx.font = 'bold 18px Cairo, sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText(title, x + 210, y + 180);
  
  // وصف قصير
  ctx.fillStyle = '#666';
  ctx.font = '14px Cairo, sans-serif';
  ctx.fillText('وصفة لذيذة وسهلة التحضير', x + 210, y + 205);
  
  // زر
  ctx.fillStyle = '#e74c3c';
  ctx.fillRect(x + 10, y + 230, 100, 30);
  ctx.fillStyle = '#fff';
  ctx.font = '14px Cairo, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('عرض الوصفة', x + 60, y + 250);
}

// رسم ثلاث بطاقات
drawRecipeCard(50, 250, 'كبسة لحم');
drawRecipeCard(290, 250, 'فتوش');
drawRecipeCard(530, 250, 'باستا بالخضار');

// تصدير الصورة
const dataUrl = canvas.toDataURL('image/png');
const img = document.createElement('img');
img.src = dataUrl;
document.body.appendChild(img);
