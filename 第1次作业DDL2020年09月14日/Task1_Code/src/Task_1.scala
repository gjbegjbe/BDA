import java.io.{File, PrintWriter}
import scala.io.Source

object Task_1 {
  def main(args: Array[String]): Unit = {
    //读文件，转换为字符串list
    val file = Source.fromFile("test.txt")
    val linesList :List[String] = file.getLines().toBuffer.toList

    //按空格切分并压平
    val words = linesList.flatMap(_.split(" "))

    //将单词转为小写
    val lowerCaseWords = words.map(_.toLowerCase())

    //将每个单词转换为元组并且分组
    val groups = lowerCaseWords.map(x=>(x,1)).groupBy(_._1)

    //对每组单词出现次数求和并转为list
    val groupsCount = groups.map(t=>(t._1,t._2.size)).toList

    //根据出现次数倒序排序
    val wordCount = groupsCount.sortBy(_._2).reverse

    //在控制台打印并写入文件
    for(x <- wordCount){
      println(x._1 + "\t" + x._2)
    }
    val writer = new PrintWriter(new File("result.txt"));
    for(x <- wordCount){
      writer.println(x._1 + "\t" + x._2)
    }
    writer.close()
  }
}
