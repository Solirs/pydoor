package main

import(

	"fmt"
	"net"
	"strings"
	"log"

)


func checkErr(err error){
	if err != nil{
		log.Fatal(err)
	}
}


func processmsg(msg string, con net.Conn){



	fmt.Println("Server got:", msg)

	cmd := strings.Fields(msg)

	switch(cmd[0]){

	default:
		con.Write([]byte("Invalid command " + cmd[0]))
	}

	





}



func main(){

	lis, err := net.Listen("tcp", ":35891")

	checkErr(err)


	for {


		con, err := lis.Accept()
		

		checkErr(err)
	
		for {
			buf := make([]byte, 4096)
			_, err := con.Read(buf)
			checkErr(err)
			processmsg(string(buf), con)
			
	    }		
}




}