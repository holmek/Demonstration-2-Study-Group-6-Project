import umqtt_robust2 as mqtt
from machine import Pin
from machine import PWM
from time import sleep
from gpio_lcd import GpioLcd

# Her kan i placere globale varibaler, og instanser af klasser

def lcd():
    lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25), d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22), num_lines=4, num_columns=20)
    lcd.clear()
    lcd.putstr("Modtaget")
    sleep(5)  
    lcd.clear()

pb1 = Pin(4, Pin.IN)

BUZZ_PIN = 26
buzzer_pin = Pin(BUZZ_PIN, Pin.OUT)
pwm_buzz = PWM(buzzer_pin)

GREEN_PIN = 13
led3 = Pin(GREEN_PIN, Pin.OUT)

def buzzer(buzzer_PWM_object, frequency, sound_duration, silence_duration):
    buzzer_PWM_object.duty(512)
    buzzer_PWM_object.freq(frequency)
    sleep(sound_duration)
    buzzer_PWM_object.duty(0)
    sleep(silence_duration)

buzzer(pwm_buzz, 262, 0.2, 0.2)
buzzer(pwm_buzz, 294, 0.4, 0.3)

while True:
    try:
        # Indskriv egen kode her:
        
        if mqtt.besked == "send":
               print("Spiller tone og lcd vises")
               buzzer(pwm_buzz, 262, 0.2, 0.2)
               buzzer(pwm_buzz, 293, 0.2, 0.2)
               buzzer(pwm_buzz, 330, 0.2, 0.2)
               buzzer(pwm_buzz, 392, 0.2, 0.2)
               lcd()
        
        if mqtt.besked == "a":
               print("Spiller tone a!")
               buzzer(pwm_buzz, 262, 0.2, 0.2)
               
        if mqtt.besked == "b":
               print("Spiller tone b!")
               buzzer(pwm_buzz, 294, 0.4, 0.3)
               
        if mqtt.besked == "led_3":
                print("led_3 lyser")
                led3(1)
        elif mqtt.besked == "led_0":
                print("led_3 slukket")
                led3(0)
                
        first = pb1.value()
        sleep(0.01)
        second = pb1.value()
        if first == 1 and second ==0:
            print("knap trykket")
        elif first == 0 and second == 1:
            print("knap sluppet")
            mqtt.web_print(1)
            sleep(3)
            mqtt.web_print(0)
            
            # Dette er en simplere måde at vise indikator lys på
            #if pb1.value() == 0:
            #  print("Knappen blev trykket")
            #    mqtt.web_print("alive")
            
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""
            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO             
        #sleep(1) # Udkommentér denne og næste linje for at se visuelt output
        #print(".", end = '') # printer et punktum til shell, uden et enter        
    
    except KeyboardInterrupt: # Stopper programmet når der trykkes Ctrl + c
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()
