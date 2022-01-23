package main

import(

	"fmt"
	"net"
	"log"
	"bufio"

)


func checkErr(err error){
	if err != nil{
		log.Fatal(err)
	}
}



func main(){



	lis, err := net.Listen("tcp", ":35891")

	checkErr(err)


	for {
		con, err := lis.Accept()

		checkErr(err)
	
		message, _ := bufio.NewReader(con).ReadString('\n')
		fmt.Print("Message Received:", string(message))
	  }




}