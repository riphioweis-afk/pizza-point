# 🍕 Pizza Point POS

![logo](images/logo.png)

##  
[Launch App](https://pizza-poin-e35c51af1aa9.herokuapp.com/)

---

>A modern Point of Sale web application built for pizza shops — allowing staff to take customer orders, send them to the kitchen, and manage the full order flow in one place.


![main](images/homePage.jpg)
PitLane provides full **CRUD functionality** (Create, Read, Update, Delete) so users can easily manage information about their cars through a clean and intuitive interface.

---

## ✨ Features

- **Full CRUD Functionality**
  - ➕ Create new vehicles
  - 👀 View saved vehicle details
  - ✏️ Edit existing car information
  - 🗑️ Delete vehicles from your garage
- **User-Friendly Interface**
  - Clean, modern UI with smooth hover effects
- **Vehicle Information Storage**
  - Save details like make, model, year, and more
- **Dynamic Updates**
  - Changes update instantly without refreshing the page
- **Responsive Design**
  - Works on desktop, tablet, and mobile devices
- **User-Based Data**
  - Each user manages their own vehicles

---

## 🛠 How to Use

1. Sign up or sign in to your account
2. Navigate to the dashboard
3. Add a new car using the “Add Vehicle” form
4. View all saved cars in your garage
5. Edit or delete vehicles as needed
6. Manage your car collection anytime

---

## ➕ Create a Vehicle

Users can add a new car by submitting vehicle details.

```javascript
router.post("/", async (req, res) => {
  try {
    console.log('Session user:', req.session.user);
    console.log('Request body:', req.body);
    
    const { make, model, year, mileage } = req.body;

    if (!make || !make.trim()) throw new Error("Make requires a proper Make");
    if (!model || !model.trim()) throw new Error("Model requires a proper Model");
    if (!year || year < 1885)
      throw new Error("Invalid year, please provide a year greater than 1885");
    if (!mileage || mileage < 0)
      throw new Error("Invalid mileage, please provide a mileage greater than 0");

    req.body.owner = req.session.user._id;
    const newVehicle = await Vehicle.create(req.body);
    console.log('Created vehicle:', newVehicle);
    
    res.redirect("/carlistings");
  } catch (error) {
    console.log('Error creating vehicle:', error);
    req.session.message = error.message;
    req.session.save(() => {
      res.redirect("/carlistings/new");
    });
  }
});
```
---
## Adding a new vehicle

Users can add a new vehicle by filling out the **Add Vehicle** form.  
Once submitted, the vehicle is saved and displayed in the user’s garage.

**Example flow:**
- Enter vehicle make
- Enter model and year
- Submit the form to save the vehicle
![add](images/add.jpg)
---
## Other resourese used 
* [Figma](https://www.figma.com/make/?gclsrc=aw.ds&&utm_source=google&utm_medium=cpc&utm_campaign=21284800681&utm_term=figma&utm_content=766100984546&utm_adgroup=169015407344&gad_source=1&gad_campaignid=21284800681&gbraid=0AAAAACTf0kPqWNpUxg3tlMOx_IYzf6QKN&gclid=Cj0KCQiAvtzLBhCPARIsALwhxdpQVOr-av0wDBYQzPY6lRnCdye5C03VQQhQDg5a8RWq8KhdnN_w7EEaAqfFEALw_wcB)
---


## Furture Enhancements
* A maintence tracker
* A cost estimator 
* A pop up for the user when filling from  
---

 ## Technologies Used
 * EJS
 * CSS
 * JavaScript
 ---