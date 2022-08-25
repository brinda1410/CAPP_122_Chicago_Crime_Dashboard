# Chicago Crime Dashboard

## Purpose

This is an interactive data visualization dashboard created using Python. It contains 3 tabs: 

1. Crime tab - A histogram displays the frequency of the crime type (selected by a user from the dropdown menu) will show across different wards.
2. Social Investment tab - A histogram displays the frequency of the type of social capital investment (selected by a user from the dropdown menu) will show across different wards.
3. Choropleth map - Visualizes the residual error from the multivariate regression of crime incidence on proxies of social investment at ward-level.

Below is a screenshot of the output from the dashboard.

<img width="909" alt="Crime Tab" src="https://user-images.githubusercontent.com/90286831/186738202-d2fc1885-bf96-412e-b79a-838ec191e14d.png">

<img width="956" alt="image" src="https://user-images.githubusercontent.com/90286831/186738281-8515ccbe-bcc3-41e8-81af-925d9658ef9b.png">


## Steps to Replicate

1. In the terminal bash, clone this project by typing the following command "git clone git@github.com:brinda1410/CAPP_122_Chicago_Crime_Dashboard.git"
2. Run the command "source install.sh" in the terminal bash
3. The install.sh will create a virtual environment and install the required packages.
4. Once the packages are installed, it will open the application automatically. 
5. With the application open, there are 3 options:
a) Option 1: Update the data by connecting with the Chicago Data Portal API.
b) Option 2: Open the interactive dashboard.
c) Option 3: Close the application. 
5. After closing the application, the virtual environment will be removed and the terminal will show a final message "Bye bye!".
