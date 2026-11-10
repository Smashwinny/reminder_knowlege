// 教学薄入口；vendor/marks.rs 为固定上游的逐字节副本。
#[path = "../vendor/marks.rs"]
mod marks;
fn main() {
    let path = std::env::args().nth(1).expect("传入 bodies.txt");
    let text = std::fs::read_to_string(path).expect("读取捕获的标记");
    for line in text.lines() {
        println!("{:?} -> {:?}", line, marks::read(line.as_bytes()));
    }
}
