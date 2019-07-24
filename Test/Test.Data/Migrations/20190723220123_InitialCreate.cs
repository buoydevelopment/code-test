using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace Test.Data.Migrations
{
    public partial class InitialCreate : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Urls",
                columns: table => new
                {
                    Id = table.Column<string>(maxLength: 128, nullable: false),
                    Start_Date = table.Column<DateTime>(nullable: true),
                    Last_Usage = table.Column<DateTime>(nullable: true),
                    IsDeleted = table.Column<bool>(nullable: true),
                    SourceUrl = table.Column<string>(nullable: true),
                    TargetUrl = table.Column<string>(nullable: true),
                    Valid = table.Column<bool>(nullable: false),
                    Code = table.Column<string>(nullable: true),
                    Usage_Count = table.Column<int>(nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Urls", x => x.Id);
                });
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Urls");
        }
    }
}
