# 💝 Valentine's Day Interactive Application

A fun and romantic web application to ask that special someone to be your Valentine!

## 🌟 Features

- **Interactive "No" Button**: The "No" button moves to random positions AND decreases in size every time someone tries to hover over it
- **Romantic Animations**: Beautiful heart confetti animations when they click "Yes"
- **Background Music**: Romantic music plays automatically (with toggle control)
- **Traditional Valentine's Theme**: Beautiful gradient background with pink, red, and white colors
- **Floating Hearts**: Animated hearts floating in the background
- **Mobile Responsive**: Works perfectly on all devices

## 🎯 How It Works

1. Open `index.html` in any web browser
2. The question "Will you be my Valentine?" is displayed
3. Try clicking "No" - it will run away and shrink! 😄
4. Click "Yes" to see romantic animations and hear music 💕

## 🚀 Usage

### Local Usage
Simply open `index.html` in your web browser:
```bash
open index.html  # macOS
start index.html  # Windows
xdg-open index.html  # Linux
```

### Deploy Online
You can deploy this to any static hosting service:
- **GitHub Pages**: Push to a repo and enable Pages
- **Netlify**: Drag and drop the folder
- **Vercel**: Deploy with one click
- **Surge.sh**: `surge valentine/`

### Share the Link
Once deployed, just share the link with your special someone! 🎁

## 🎨 Customization

### Change the Music
Replace the audio source URL in line ~234:
```html
<source src="YOUR_MUSIC_URL.mp3" type="audio/mpeg">
```

### Change the Success Message
Edit the romantic message in the HTML (lines ~197-202):
```html
<p class="romantic-message">
    Your custom message here! 💖
</p>
```

### Change Colors
Modify the background gradient in the CSS (lines ~14-19):
```css
background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 50%, #fbc2eb 100%);
```

### Change the GIF
Replace the Giphy URL on line ~203 with your preferred romantic GIF.

## 📱 Browser Compatibility

Works on all modern browsers:
- ✅ Chrome/Edge
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Mobile browsers

## 💡 Tips

- The "No" button will shrink each time they hover over it
- After several hover attempts, the "Yes" button grows bigger
- After 7+ hover attempts, the "No" button turns into a sad emoji
- Music toggle button appears in the bottom-right corner

## ❤️ Made with Love

Perfect for:
- Valentine's Day surprises
- Romantic proposals
- Cute date invitations
- Just making someone smile! 😊

---

**Happy Valentine's Day! 💕**
