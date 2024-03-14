# ASHOK LEYLAND HEALTH ESTIMATION 



## File Description:
    
    'Training Module: driver.py'
    'Inference/Testing Module: inference.py' 
    'Inference/Testing Module: retraining.py' 

`NOTE: ALL COMMANDS ARE COMMA SEPERATED PLEASE FOLLOW THE SPACING DEPICTED BELOW`  
    
## Training Script Example:

### Arguments:

    '--Vehicle_List: Enter the vehicle names with a space in between; nargs='+', type=str,help='For master model enter all the vehcile models required'
    '--Model: Give an appropriate Model name Vehicle Name/Master Model; type=str,help='Depicts the vehicle model master/individual'

` Command: python driver.py --Vehicle_List G423 --Model G423 `


### Output :
   ![alt text](/results_images/train.jpg)

   
> The vehicle's health is estimated from the given vehicle parameters fed to the model
   ![alt text](/results_images/health.jpg)

## Inference Script Example:

### Arguments:

    '--Model',type=str,help='Depicts the vehicle model master/individual'
    '--Data',type=str,help='New Data File Name; type=str,help='New Data File Name'

` Command: python inference.py --Data G423_Test --Model G423 `

### Output :
   ![alt text](/results_images/inference.png)

## Retraining Script Example:

### Arguments:

    '--Model',type=str,help='Depicts the vehicle model master/individual'
    '--Data',type=str,help='New Data File Name; type=str,help='New Data File Name'

` Command: python retrainning.py --Data G423_new --Model G423 `
### Output :
   ![alt text](/results_images/retrain.png)
