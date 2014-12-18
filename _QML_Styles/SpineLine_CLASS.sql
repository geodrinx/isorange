

update EFA_SpineLine set IdClass = '781_1'
 where COD_VARIET = '781' and cast(misura as integer) >= 0.00 and cast(misura as integer) <= 2.00;

update EFA_SpineLine set IdClass = '781_2'
 where COD_VARIET = '781' and cast(misura as integer) >= 2.001 and cast(misura as integer) <= 6.00;

update EFA_SpineLine set IdClass = '781_3'
 where COD_VARIET = '781' and cast(misura as integer) >= 6.0001 and cast(misura as integer) <= 9.00;
 
update EFA_SpineLine set IdClass = '781_4'
 where COD_VARIET = '781' and cast(misura as integer) >= 9.0001 and cast(misura as integer) <= 20.00;

update EFA_SpineLine set IdClass = '781_5'
 where COD_VARIET = '781' and cast(misura as integer) >= 20.0001 and cast(misura as integer) <= 100000.00; 
 
 
update EFA_SpineLine set IdClass = '782_1'
 where COD_VARIET = '782' and cast(misura as integer) >= 0.00 and cast(misura as integer) <= 2.00;

update EFA_SpineLine set IdClass = '782_2'
 where COD_VARIET = '782' and cast(misura as integer) >= 2.001 and cast(misura as integer) <= 6.00;

update EFA_SpineLine set IdClass = '782_3'
 where COD_VARIET = '782' and cast(misura as integer) >= 6.0001 and cast(misura as integer) <= 9.00;
 
update EFA_SpineLine set IdClass = '782_4'
 where COD_VARIET = '782' and cast(misura as integer) >= 9.0001 and cast(misura as integer) <= 20.00;

update EFA_SpineLine set IdClass = '782_5'
 where COD_VARIET = '782' and cast(misura as integer) >= 20.0001 and cast(misura as integer) <= 100000.00;     
