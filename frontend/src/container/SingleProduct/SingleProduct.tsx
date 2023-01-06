import * as React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import Radio from "@mui/material/Radio";
import { CardActionArea } from "@mui/material";
import ButtonGroup from "@mui/material/ButtonGroup";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import Grid from "@mui/material/Unstable_Grid2";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import ShoppingBagTwoToneIcon from "@mui/icons-material/ShoppingBagTwoTone";

import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, EffectFade } from "swiper";
import "swiper/css/navigation";
import "swiper/css/effect-fade";
import "swiper/css"

import iphone_pro_max_black from "../../Images/iph_14_pro_max.png";
import iphone_pro_max_silver from "../../Images/iph_14_pro_max_silver.png";
import iphone_pro_max_deep_purple from "../../Images/iph_14_pro_max_purple.png";
import iphone_pro_max_gold from "../../Images/iph_14_pro_max_gold.png";
import "./SingleProduct.css";

interface iMemoryCard {
  sizeStr: string;
  priceStr: {
    line1: string;
    line2: string;
    line3: string;
  };
  item: string;
}

const PriceCard = ({
  mcard,
  selectedValue,
  setSelectedValue,
}: {
  mcard: iMemoryCard;
  selectedValue: string;
  setSelectedValue: any;
}) => {
  const handleChange = () => {
    setSelectedValue(mcard.item);
  };
  return (
    <Card
      id="ID"
      sx={{
        maxWidth: 500,
        borderRadius: 4,
        borderWidth: selectedValue === mcard.item ? 5 : 0,
        borderStyle: "solid",
        borderColor: "black",
      }}
      onClick={handleChange}
    >
      <CardActionArea sx={{ display: "flex" }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography component="div" variant="h5">
            {mcard.sizeStr}
          </Typography>
        </CardContent>

        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography variant="body2" align="right">
            {mcard.priceStr.line1}
            <br />
            {mcard.priceStr.line2}
            <br />
            {mcard.priceStr.line3}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

function App() {
  const [selectedValue, setSelectedValue] = React.useState("z");

  const [cardSelectedVal, setCardSelectedVal] = React.useState("z");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedValue(event.target.value);
  };

  const controlProps = (item: string) => ({
    checked: selectedValue === item,
    onChange: handleChange,
    value: item,
    name: "color-radio-button-demo",
    inputProps: { "aria-label": item },
  });

  const memoryCards: iMemoryCard[] = [
    {
      sizeStr: "128 GB",
      priceStr: {
        line1: "From $1099",
        line2: "or $45.79/mo.per month for 24 mo.",
        line3: "before trade‑in*",
      },
      item: "e",
    },
    {
      sizeStr: "256 GB",
      priceStr: {
        line1: "From $1199",
        line2: "or $49.95/mo.per month for 24 mo.",
        line3: "before trade‑in*",
      },
      item: "f",
    },
    {
      sizeStr: "512 GB",
      priceStr: {
        line1: "From $1399",
        line2: "or $58.29/mo.per month for 24 mo.",
        line3: "\n before trade‑in*",
      },
      item: "g",
    },
    {
      sizeStr: "1 TB",
      priceStr: {
        line1: "From $1599",
        line2: "or $66.62/mo.per month for 24 mo.",
        line3: "\n before trade‑in*",
      },
      item: "h",
    },
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1> Buy Iphone 14 pro </h1>

        <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={2} disableEqualOverflow>
            <Grid xs={8} style={{ maxHeight: "100%", overflow: "hidden" }}>
              {/* <img src={iphone_pro_max_black} className="myImg" alt="logo" /> */}
              <div className="swiper-container">
                <Swiper
                  modules={[Navigation, EffectFade]}
                  navigation
                  effect={"fade"}
                  speed={800}
                  slidesPerView={1}
                  loop
                >
                  <SwiperSlide className="swiper-slide">
                    <img className="myImg" src={iphone_pro_max_black} alt="" />
                  </SwiperSlide>

                  <SwiperSlide className="swiper-slide">
                    <img className="myImg" src={iphone_pro_max_silver} alt="" />
                  </SwiperSlide>

                  <SwiperSlide className="swiper-slide">
                    <img
                      className="myImg"
                      src={iphone_pro_max_deep_purple}
                      alt=""
                    />
                  </SwiperSlide>

                  <SwiperSlide className="swiper-slide">
                    <img className="myImg" src={iphone_pro_max_gold} alt="" />
                  </SwiperSlide>
                </Swiper>
              </div>
            </Grid>

            <Grid xs={4}>
              <List style={{ maxHeight: "100%", overflow: "auto" }}>
                <h3> Select your favourite color </h3>

                <p> Color </p>

                <div>
                  <Radio
                    {...controlProps("a")}
                    sx={{
                      color: "#CBCBCB",
                      "&.Mui-checked": {
                        color: "#CBCBCB",
                      },
                      "& .MuiSvgIcon-root": {
                        fontSize: 60,
                      },
                    }}
                  />

                  <Radio
                    {...controlProps("b")}
                    sx={{
                      color: "#602f6b",
                      "&.Mui-checked": {
                        color: "#602f6b",
                      },
                      "& .MuiSvgIcon-root": {
                        fontSize: 60,
                      },
                    }}
                  />
                  <Radio
                    {...controlProps("c")}
                    sx={{
                      color: "#FFD700",
                      "&.Mui-checked": {
                        color: "#FFD700",
                      },
                      "& .MuiSvgIcon-root": {
                        fontSize: 60,
                      },
                    }}
                  />
                  <Radio
                    {...controlProps("d")}
                    sx={{
                      color: "#111111",
                      "&.Mui-checked": {
                        color: "#111111",
                      },
                      "& .MuiSvgIcon-root": {
                        fontSize: 60,
                      },
                    }}
                  />
                </div>

                <div className="mySection">
                  <h3> Select how much storage do you need? </h3>

                  {memoryCards.map((mcard: iMemoryCard, ind: number) => {
                    return (
                      <PriceCard
                        mcard={mcard}
                        setSelectedValue={setCardSelectedVal}
                        selectedValue={cardSelectedVal}
                      />
                    );
                  })}
                </div>

                <br />
                <br />

                <ButtonGroup
                  variant="contained"
                  aria-label="outlined primary button group"
                >
                  <div className="rowSection">
                    <Button size="large">
                      <ShoppingCartIcon />
                      Add to Cart
                    </Button>
                    <Button size="large">
                      <ShoppingBagTwoToneIcon />
                      Buy now
                    </Button>
                  </div>
                </ButtonGroup>
              </List>
            </Grid>
          </Grid>
        </Box>

        <h3> Discription </h3>
        <ol type="1">
          <li>
            The display has rounded corners that follow a beautiful curved
            design, and these corners are within a standard rectangle. When
            measured as a standard rectangular shape, the screen is 5.42 inches
            (iPhone 13 mini), 6.06 inches (iPhone 13, iPhone 14), 6.12 inches
            (iPhone 14 Pro), 6.68 inches (iPhone 14 Plus), or 6.69 inches
            (iPhone 14 Pro Max) diagonally. Actual viewable area is less.
          </li>
          <li>
            Available space is less and varies due to many factors. A standard
            configuration uses approximately 12GB to 17GB of space, including
            iOS 16 with its latest features and Apple apps that can be deleted.
            Apple apps that can be deleted use about 4.5GB of space, and you can
            download them back from the App Store. Storage capacity subject to
            change based on software version, settings, and iPhone model.
          </li>
          <li>
            Service is included for free for two years with the activation of
            any iPhone 14 model. Connection and response times vary based on
            location, site conditions, and other factors. See
            apple.com/iphone-14(Opens in a new window) or
            apple.com/iphone-14-pro(Opens in a new window) for more information.
          </li>
          <li>
            All battery claims depend on network configuration and many other
            factors; actual results will vary. Battery has limited recharge
            cycles and may eventually need to be replaced. Battery life and
            charge cycles vary by use and settings. See apple.com/us/batteries
            and apple.com/us/iphone/battery.html for more information.
          </li>
          <li>
            Data plan required. 5G is available in select markets and through
            select carriers. Speeds vary based on site conditions and carrier.
            For details on 5G support, contact your carrier and see
            apple.com/iphone/cellular.
          </li>
        </ol>
      </header>
    </div>
  );
}

export default App;
