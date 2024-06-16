import solcx

solcx.install_solc ( "0.8.2" )

result = solcx.compile_source (
    "contract Foo { function bar ( ) public { return; } }",
    output_values = ["abi", "bin-runtime"],
    solc_version = "0.8.2"
)

print ( result )