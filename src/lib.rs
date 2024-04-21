use serde::Deserialize;
use std::{fs, io::Write};

pub trait Format {
    fn format(&self) -> String;
}

pub fn write_into_csv<'a, T>(index: usize, objects: Vec<T>) -> Box<dyn Fn() -> ()>
where
    T: Deserialize<'a> + Format + 'static,
{
    Box::new(move || {
        let mut file = fs::File::options()
            .append(true)
            .create(true)
            .open(format!("assets/example/output/{index}.csv"))
            .unwrap();

        if index == 1 {
            let _ = writeln!(&mut file, "id,name");
        }

        for line in objects.iter() {
            let _ = writeln!(&mut file, "{}", line.format());
        }
    })
}
