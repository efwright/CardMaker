#Card Maker Language (CML)

You must define the size of the card using:

```
  card_size(width, height);
```

CML has several pre-defined types to use. These types are:  

* Image
* Imagebox
* Text
* Textbox

To declare a variable of a type, you must have the type, followed by a unique name, ended by a semicolon. Here is an example:

```
  Image image1;
  Image image2;
  Image image3;
  Imagebox imagebox1;
  Text text1;
  Text text2;
  Textbox textbox1;
```

The order that these variables are declared in will define in what order they show up on the card. The variable declared last will be on-top of everything else.

These variables must be declared first before they can have values set to them.

To set an Image, you must use must use one of these functions calls:

```
  image1 = read_image("filename");
  image2 = crop_image("filename", x, y, width, height);
  image3 = scale_image("filename", width, height);
```

An Imagebox is comprised of an Image, and a bounding box, and an opacity. You must set this individually like this:

```
  imagebox1.image = image1;
  imagebox1.box = (x, y, width, height);
  imagebox1.opacity = 50;
```

If the width or height is 0, then it will be assumed that is is the same as the width and height of the Image. If the width and height are not 0, and their values are different than the Image's width and height a warning will be emitted.

The opacity must be a number between 1 and 100, with 100 being fully opaque. If no opacity is set, then 100 is used.

To set a Text:

```
  text1 = "This is my text.";
```

For some cards you may want to use symbols in place of text characters. When you run this program, you may give it a file containing all valid symbols. You may use symbols like this:

```
  text2 = "This is a text with $(symbol1) a symbol."
```

To set a Textbox, you have to set individual parts of it. A Textbox consists of a list of Text, a bounding box, a font, and a font size. You may set all of those values of a Textbox like this:

```
  textbox1.text = [text1, text2];
  textbox1.box = (x, y, width, height);
  textbox1.font = "font"
  textbox1.fontsize = size;
```

You may also inherent variables from other card files. This may be useful when you are making a bunch of cards that have similar formatting. To do this, you do so like this:

```
  use "othercard.card";
```

To add comments, you may use:

```
  Image image1; # This is a comment.
```

Here is an example card using a template:

```
  # TemplateCard.card

  card_size(200, 200);

  Image artwork;
  Imagebox artbox;
  Text name;
  Textbox namebox;

  artbox.image = artwork;
  artbox.box = (50, 75, 100, 100);
  artbox.opacity = 100;

  namebox.text = [name];
  namebox.box = (0, 0, 100, 20);
  namebox.font = "Arial";
  namebox.fontsize = 18;

  # MyCard.card

  use "TemplateCard.card"

  artwork = crop_image("myimage.png", 0, 0, 100, 100);
  name = "My Card";
```
