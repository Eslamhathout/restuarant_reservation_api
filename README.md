# restuarant_reservation_api

### How to start
    The system has two services one for postgres and the other one for the core container.
    You have to install docker and navigate to the reservation/docker-compose file, then run:
    $docker-compose build
    $docker-compose up

    $docker-compose run app sh -c "python manage.py migrate" #For running the migrations
    $docker-compose run app sh -c "python manage.py shell" #For accessing the shell


### Functional requirements. 
    ####### Users & Authentication
    My system satifies the need for creating both employee nad admin staff.
    For the purpose of testing I created two types of users: 
        employee: i.hathout94@gmail.com



![alt text](https://imgur.com/CGfSPnO.png)



        admin: i.a.hathout@gmail.com



![alt text](https://imgur.com/YMzU8BA.png)



    so verify with each screen whcih user is logged in 
    TODO: screen for each user email


    ####### Table Management
        Desc: Admins can use this API to get the current list of tables, add new table, or delete any existing table with no pending reservations.
        API: /api/reservation/tables/
        Users: As this is restricted from employees and only allowed for admins. I implemented a permission to control this view:
            * Employee



![alt text](https://imgur.com/e05FAnp.png "employee_table")



            * Admin



![alt text](https://imgur.com/9h12iXE.png "table_table")




                Attepmts to delete a table with pending reservations:



![alt text](https://imgur.com/undefined.png)




![alt text](https://imgur.com/1E1eOD2.png)




    ####### Reservations
        NOTE: For simplicity I limited the availble slots to only 3 days, the minimum slot is 15 minutes, and opening_hours between (13, 23).
                You can tweek these settings from utils.constants.py file.
        * Check available time slots
            Desc: You can use this API to get available time-slots based on any given date and number_of_persons.
            API: /api/reservation/check/
            Users: As both employees and admins can check availability. here is the check for 4 places in sep 5th.




![alt text](https://imgur.com/hemqW9y.png)




            Sample_output: {
                            "message": "Available slot for the tables that fits the required number of people sorted by bestFit first.",
                            "data": {
                                "2021-09-05": [
                                    {
                                        "table_number": 2,
                                        "table_capacity": 4,
                                        "table_availability": [
                                            "21:38 - 22:00"
                                        ]
                                    },
                                    {
                                        "table_number": 8888,
                                        "table_capacity": 6,
                                        "table_availability": [
                                            "21:38 - 23:00"
                                        ]
                                    }
                                ]
                            }
                        }
        
            Outliers:
                deny any capacity more than 12




![alt text](https://imgur.com/undefined.png)




        * Reserve a time slot
            Desc: You can use this API to get reserve a time-slot.
            API: /api/reservation/reserve/
            Users: Both employees and admins can reserve a time-slot.



![alt text](https://imgur.com/RkWadBm.png)



            Outliters:
                - Attepmt to reserve a table with more than it's capacity




![alt text](https://imgur.com/undefined.png)




                - Attempt tp reserve a table in the past or far from 3 days max




![alt text](https://imgur.com/2hLbtKQ.png)



        * Get reservations for today
            Desc: You can use this API to get all reservation for current date.
            API: /api/reservation/todays-reservations/
            Users: Both employees and admins can get a list of current_day reservations.
            Enhancments: Add ordering and paggingation 




![alt text](https://imgur.com/undefined.png)



        * Get all reservations
            Desc: You can use this API to get all reservation.
            API: /api/reservation/reservations-list/
            Users: Only admins can get the list of reservations.




![alt text](https://imgur.com/5D9VUb0.png)





            Outliters: Employee can not get the list of reservations





![alt text](https://imgur.com/GY2z0JY.png)





        * Delete a reservation
            Desc: You can use this API to delete a reservation by ID.
            API: /api/reservation/reservation-destory/19/
            Users: Both employees and admins can delete a reservation in the future.



![alt text](https://i.imgur.com/vvNYET3.png)

