content = '''<div align="center"> <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0D1117,50:161B22,100:0D1117&height=200&section=header&text=van1dal&fontSize=60&fontColor=00ADD8&fontAlignY=42&desc=Backend%20Developer%20%E2%80%A2%20Go%20%2F%20Backend&descAlignY=62&descSize=17&descColor=5DC9E2&animation=fadeIn"/> <a href="https://github.com/van1dal"> <img src="https://readme-typing-svg.demolab.com?font=Google+Sans&weight=500&size=22&duration=3000&pause=1200&color=00ADD8&center=true&vCenter=true&width=560&lines=Building+reliable+backend+systems;Go+%2B+PostgreSQL+%2B+REST+APIs;Designing+clean+backend+services" alt="Typing SVG" /> </a> </div> <br>

About

<table> <tr> <td width="55%" valign="top">

Backend developer building well-structured, production-minded services with Go. Focused on clean API design, relational data modeling, concurrency, and the operational side of software — containers, Linux, and cloud infrastructure.

Currently moving from "it works" to "it's built to last."

Focus      Backend Engineering

Learning   REST APIs · Concurrency · System Design

Ask me     Go · Backend · SQL

</td> <td width="45%" valign="top">

```go

package main

type Engineer struct {

    Name  string

    Role  string

    Stack []string

}

func (e Engineer) Philosophy() string {

    return "Simple, readable, " +

        "and correct — " +

        "in that order."

}

```

</td> </tr> </table> <br>

Tech Stack

<table> <tr> <td valign="top" width="33%">

Language & Framework

<img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/Gin-00ADD8?style=for-the-badge&logo=gin&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/GORM-00ADD8?style=for-the-badge&logo=go&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/REST%20API-5DC9E2?style=for-the-badge&logo=fastapi&logoColor=white" height="28"/>

</td> <td valign="top" width="33%">

Data

<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/MySQL-FBBC05?style=for-the-badge&logo=mysql&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/SQL-EA4335?style=for-the-badge&logo=databricks&logoColor=white" height="28"/>

</td> <td valign="top" width="33%">

Infrastructure

<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/Linux-EA4335?style=for-the-badge&logo=linux&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/Google%20Cloud-34A853?style=for-the-badge&logo=googlecloud&logoColor=white" height="28"/><br> <img src="https://img.shields.io/badge/Git-FBBC05?style=for-the-badge&logo=git&logoColor=white" height="28"/>

</td> </tr> </table> <br>

Engineering Journey

<div align="center"> <img src="https://img.shields.io/badge/01-Go%20Core-161B22?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/02-Structs%20%26%20Interfaces-161B22?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/03-Concurrency-161B22?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/04-HTTP%20%26%20REST-161B22?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/05-Backend%20Architecture-00ADD8?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/06-Database%20Design-252B33?style=flat-square" height="34"/>

↓

<img src="https://img.shields.io/badge/07-Cloud-252B33?style=flat-square" height="34"/> <br> <img src="https://readme-typing-svg.demolab.com?font=Google+Sans&weight=400&size=15&duration=2500&pause=1500&color=5DC9E2&center=true&vCenter=true&width=460&lines=Currently+at%3A+Go+backend+development+%26+REST+API+design" alt="Current stage"/> </div> <br> <div align="center"> <a href="https://github.com/van1dal"> <img src="https://img.shields.io/badge/-GitHub-00ADD8?style=for-the-badge&logo=github&logoColor=white" height="30"/> </a>

<sub>© van1dal — Backend Developer</sub>

</div>

'''

path = "/mnt/data/README.md"

with open(path, "w", encoding="utf-8") as f:

    f.write(content)

print(path)
