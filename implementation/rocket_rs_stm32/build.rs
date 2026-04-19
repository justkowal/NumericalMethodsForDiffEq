use std::{env, fs, path::PathBuf};

fn main() {
    println!("cargo:rerun-if-env-changed=ROCKET_STEP_SIZE");

    let step_size_raw = env::var("ROCKET_STEP_SIZE").unwrap_or_else(|_| "0.1".to_string());

    let step_size: f32 = step_size_raw.parse().unwrap_or_else(|_| {
        panic!(
            "ROCKET_STEP_SIZE must be a valid float in seconds, got: {}",
            step_size_raw
        )
    });

    assert!(
        step_size > 0.0,
        "ROCKET_STEP_SIZE must be > 0.0, got {}",
        step_size
    );

    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR not set"));
    let generated = out_dir.join("step_size.rs");

    fs::write(
        generated,
        format!(
            "pub const STEP_SIZE: f32 = {step_size}f32;\n"
        ),
    )
    .expect("failed to write generated step_size.rs");
}
