package kr.hull.shop.controller;

import kr.hull.shop.dto.UserDto;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/req")
public class DefaultReqController {
    //http://localhost:8080/req/html
    @RequestMapping(value = "/html", method = RequestMethod.GET)
    public String html() {
        return "get/index";
    }

    //http://localhost:8080/req/html/안녕하세요
    @RequestMapping(value = "/html/{msg}", method = RequestMethod.GET)
    public String html(@PathVariable String msg, Model m) {
        m.addAttribute("msg", msg);
        return "get/index";
    }

    //http://localhost:8080/req/txt?msg=안녕하세요
    @RequestMapping(value = "/txt", method = RequestMethod.GET)
    @ResponseBody
    public String html(@RequestParam(value="msg", required=false) String msg) {
        return msg;
    }

    //http://localhost:8080/req/json
    @RequestMapping(value = "/json", method = RequestMethod.GET)
    @ResponseBody
    public ResponseEntity<Object> html(Model m) {
        m.addAttribute("model","모델값 json");
        return new ResponseEntity<>(m, HttpStatus.OK);
    }

    //http://localhost:8080/post.html -> http://localhost:8080/req/dto
    // POST : name=홍길동&phone=01011111111 -> userDto
    @RequestMapping(value = "/dto",  method = RequestMethod.POST)
    @ResponseBody
    public UserDto html(UserDto userDto) {
        return userDto;
    }

    //http://localhost:8080/post.html -> http://localhost:8080/req/dto-model
    // POST : name=홍길동&phone=01011111111 -> userDto
    @RequestMapping(value = "/dto-model", method = RequestMethod.POST)
    public String html(UserDto userDto, Model m) {
        m.addAttribute("dto", userDto);
        return "post/index";
    }
}
